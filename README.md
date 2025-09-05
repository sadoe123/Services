output_templates/ (Contient les templates des services)
│── ${FunctionId}IRAPFormService.java.j2
│── ${FunctionId}IRAPListBlockService.java.j2
│── ${FunctionId}FunctionService.java.j2

la géneration de IRAP_Services Templates est composé de deux parties :

Script 1 : création des templates .j2 dans output_templates/. FormService,GridService ,FunctionService 
Script 2 : génération du code Java final dans output/


la génération LOV Service Template(Jinja2):
Le template généré est un fichier XML Spring .j2

Les beans sont construits selon le champ isWithParam :

  isWithParam = True → entries dans genericLovQueryService.
  isWithParam = False → beans individuels pour chaque LOV.

Le fichier générés sont stockés dans le dossier output_templates/(lov_service_impl.spring.xml.j2)