#  -----------------------------------------------------------------------------
#  GPTranslator 2024
#  Ce logiciel en python a été développé dans le cadre du concours "Trophées NSI"
#  
#  Application python pour transferré les traductions d'un langue a l'autre
#  
#  -----------------------------------------------------------------------------           
#                     
#  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 
#  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@          
#  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                  
#  @@@@@@@@@@@@@@@@@@@@@@@@@                             
#  @@@@@@@@@@@@@@@@@@@@@@                 
#              @@@@@@@@                    
#              @@@@@@                      
#              @@@@@                       
#              @@@@                        
#              @@@                         
#               @                          
#   

import json

input_file = "LngDB-ht.json"
output_file = "LngDB-fr.json"

with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

sorted_data = {k: data[k] for k in sorted(data)}

inverted_data = {v: k for k, v in sorted_data.items()}
sorted_inverted_data = {k: inverted_data[k] for k in sorted(inverted_data)}

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(sorted_inverted_data, f, indent=4, ensure_ascii=False)

print("Inversion de l'ordre terminée. Le résultat est enregistré dans", output_file)


