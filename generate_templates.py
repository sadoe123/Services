import os
from jinja2 import Environment, FileSystemLoader

TEMPLATE_DIR = "output_templates"
OUTPUT_DIR = "output"

def capitalize_first(s):
    return s[0].upper() + s[1:] if s else s

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), trim_blocks=True, lstrip_blocks=True)

def generate_code(fct_name):
    FunctionId = capitalize_first(fct_name)
    functionId = fct_name.lower()

    # Templates disponibles dans output_templates
    templates = [
        "${FunctionId}FunctionService.java.j2",
        "${FunctionId}IRAPFormService.java.j2", 
        "${FunctionId}IRAPListBlockService.java.j2"
    ]

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for template_name in templates:
        try:
            # Charger le template
            template = env.get_template(template_name)
            
            # Rendre le template avec les variables
            content = template.render(FunctionId=FunctionId, functionId=functionId)
            
            # Déterminer le nom du fichier de sortie
            output_filename = template_name.replace(".j2", "").replace("${FunctionId}", FunctionId)
            output_file = os.path.join(OUTPUT_DIR, output_filename)
            
            # Écrire le contenu dans le fichier
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(content)
            
            print(f"✅ Fichier généré : {output_file}")
            
        except Exception as e:
            print(f"❌ Erreur lors de la génération de {template_name}: {e}")

if __name__ == "__main__":
    fct_name = input("🔧 Entrez le nom de la fonction (ex: reiv) : ").strip()
    generate_code(fct_name)
