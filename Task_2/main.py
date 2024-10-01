import requests
import yaml
import zipfile
import re
import subprocess
import os

def load_config(path):
    with open(path, 'r') as file:
        return yaml.safe_load(file)

def download_nuget_package(nuget_url, path):
    response = requests.get(nuget_url)

    if response.status_code == 200:
        with open(path, 'wb') as f:
            f.write(response.content)
        return path
    else:
        return None

def get_dependencies(package_path):
    dependencies = []
    with zipfile.ZipFile(package_path, 'r') as zip_ref:
        for file_info in zip_ref.infolist():
            if file_info.filename.endswith('.nuspec'):
                with zip_ref.open(file_info) as nuspec_file:
                    nuspec_content = nuspec_file.read()
                    dependencies = parse_nuspec(nuspec_content)
                break
    return dependencies

def parse_nuspec(nuspec_content):
    nuspec_text = nuspec_content.decode('utf-8')

    dependency_pattern = r'<dependency id="([^"]+)"'
    dependencies = re.findall(dependency_pattern, nuspec_text)

    return set(dependencies)

def generate_dot_graph(package_name, dependencies):
    dot = 'digraph G {\n'
    dot += '    graph [layout=neato, overlap=false, splines=true];\n'
    dot += f'    "{package_name}"\n'
    for dep in dependencies:
        dot += f'    "{dep}" -> "{package_name}";\n'
    dot += '}'
    return dot

def visualize_graph(visualizer_path, dot_graph):
    file_path = os.path.join(os.getcwd(), 'graph.dot')
    with open(file_path, 'w', encoding='utf-8') as dot_file:
        dot_file.write(dot_graph)

    output_png = os.path.join(os.getcwd(), 'graph.png')
    subprocess.run([visualizer_path, '-Tpng', file_path, '-o', output_png], check=True)

    print(f"Граф зависимостей сохранен в: {output_png}")

def download_and_get_deps(url, path, deps):
    package_name = str(url.split("/")[6])
    print(f"[i] Скачиваю пакет {package_name} для анализа зависимостей")
    download_nuget_package(url, path)
    dependencies = get_dependencies(path)
    for dep in dependencies:
        if dep in deps:
            continue
        deps.append(dep)
        download_and_get_deps(f"https://www.nuget.org/api/v2/package/{dep}", "./temp/package.nupkg", deps)
    return deps

if __name__ == "__main__":
    config = load_config("config.yaml")
    package_name = str(config["repository_url"].split("/")[6])

    print("Визуализация графа зависимостей для пакета: ", package_name)
    dependencies = download_and_get_deps(
        config["repository_url"],
        config["package_path"],
        [],
    )
    
    print("[i] Построение графа ...")
    dot_graph = generate_dot_graph(package_name, dependencies)
    visualize_graph(config['visualizer_path'], dot_graph)
