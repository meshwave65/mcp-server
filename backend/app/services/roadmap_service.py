# sofia/backend/app/services/roadmap_service.py (Sua Versão Final Integrada)
from sqlalchemy.orm import Session
from sqlalchemy import text
from collections import defaultdict

def get_full_roadmap(db: Session):
    # Sua consulta otimizada
    query = text("""
        SELECT
            s.value AS segment_name,
            p.value AS phase_name,
            m.id AS module_id,
            m.name AS module_name,
            m.status AS module_status
        FROM
            modules m
        JOIN
            module_metadata mm_s ON m.id = mm_s.module_id
        JOIN
            metadata_values s ON mm_s.metadata_value_id = s.id AND s.type_id = (SELECT id FROM metadata_types WHERE name = 'Segmento')
        JOIN
            module_metadata mm_p ON m.id = mm_p.module_id
        JOIN
            metadata_values p ON mm_p.metadata_value_id = p.id AND p.type_id = (SELECT id FROM metadata_types WHERE name = 'Fase')
        ORDER BY
            s.id, p.id, m.id;
    """)
    
    try:
        result = db.execute(query).mappings().all()
        
        # Sua lógica de processamento para aninhar os dados
        roadmap_data = defaultdict(lambda: defaultdict(list))
        for row in result:
            segment_name = row['segment_name']
            phase_name = row['phase_name']
            module = { "id": row['module_id'], "name": row['module_name'], "status": row['module_status'] }
            roadmap_data[segment_name][phase_name].append(module)
            
        output = []
        for segment_name, phases in roadmap_data.items():
            segment_obj = {"segment_name": segment_name, "phases": []}
            for phase_name, modules in phases.items():
                phase_obj = {"phase_name": phase_name, "modules": modules}
                segment_obj["phases"].append(phase_obj)
            output.append(segment_obj)
            
        return output
    except Exception as e:
        print(f"ERRO CRÍTICO no roadmap_service ao executar a consulta: {e}")
        return []

