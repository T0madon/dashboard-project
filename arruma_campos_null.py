import psycopg2
from psycopg2 import Error

def corrigir_departamentos_com_multiplos_ids():
    try:
        # Conectando ao banco de dados
        connection = psycopg2.connect(
            database="banco2",
            host="localhost",
            user="postgres",
            password="Gumattos2",
            port="5432"
        )
        
        cursor = connection.cursor()
        
        tabelas = [
            'artigos',
            'bolsas', 
            'congressos',
            'financiados',
            'orientacoes',
            'projetos'
        ]
        
        total_corrigidos = 0
        
        for tabela in tabelas:
            print(f"\n🔧 Corrigindo tabela: {tabela}")
            
            # Buscar registros problemáticos
            cursor.execute(f"""
                SELECT nome, id_professor, departamento 
                FROM {tabela} 
                WHERE (departamento NOT LIKE '%Departamento%' 
                   OR departamento IS NULL 
                   OR departamento LIKE '%None%'
                   OR departamento = '')
                   AND id_professor IS NOT NULL
            """)
            
            registros_problematicos = cursor.fetchall()
            print(f"Encontrados {len(registros_problematicos)} registros problemáticos")
            
            corrigidos_tabela = 0
            
            for registro in registros_problematicos:
                nome_registro = registro[0]
                id_professor_str = registro[1]  # Pode ser string com múltiplos IDs
                departamento_atual = registro[2]
                
                # Separar os IDs por vírgula e pegar o primeiro ID válido
                ids_professores = []
                if id_professor_str:
                    ids_professores = [id.strip() for id in id_professor_str.split(',') if id.strip()]
                
                departamento_correto = None
                
                # Tentar encontrar um professor válido na lista de IDs
                for id_professor in ids_professores:
                    try:
                        # Buscar departamento do professor
                        cursor.execute("""
                            SELECT departamento FROM professores 
                            WHERE id_professor = %s AND departamento LIKE '%Departamento%'
                        """, (id_professor,))
                        
                        resultado = cursor.fetchone()
                        
                        if resultado and resultado[0]:
                            departamento_correto = resultado[0]
                            break  # Usar o primeiro departamento válido encontrado
                    
                    except Exception as e:
                        print(f"Erro ao buscar professor {id_professor}: {e}")
                        continue
                
                # Se não encontrou nenhum professor com departamento válido, tentar qualquer um
                if not departamento_correto:
                    for id_professor in ids_professores:
                        try:
                            cursor.execute("""
                                SELECT departamento FROM professores WHERE id_professor = %s
                            """, (id_professor,))
                            
                            resultado = cursor.fetchone()
                            if resultado and resultado[0]:
                                departamento_correto = resultado[0]
                                break
                        
                        except Exception as e:
                            continue
                
                if departamento_correto:
                    # Atualizar somente se for diferente
                    if departamento_atual != departamento_correto:
                        cursor.execute(f"""
                            UPDATE {tabela} 
                            SET departamento = %s 
                            WHERE nome = %s AND id_professor = %s
                        """, (departamento_correto, nome_registro, id_professor_str))
                        
                        print(f"✅ Corrigido: {nome_registro[:50]}...")
                        print(f"   IDs: {ids_professores}")
                        print(f"   De: '{departamento_atual}'")
                        print(f"   Para: '{departamento_correto}'")
                        print()
                        
                        corrigidos_tabela += 1
                        total_corrigidos += 1
                else:
                    print(f"⚠️  Nenhum professor válido encontrado para: {nome_registro[:50]}...")
                    print(f"   IDs: {ids_professores}")
                    print()
            
            connection.commit()
            print(f"Tabela {tabela}: {corrigidos_tabela} registros corrigidos")
        
        print(f"\n🎉 Total de registros corrigidos: {total_corrigidos}")
        
    except (Exception, Error) as error:
        print("❌ Erro:", error)
        if connection:
            connection.rollback()
    finally:
        if connection:
            cursor.close()
            connection.close()

# Executar a correção
if __name__ == "__main__":
    corrigir_departamentos_com_multiplos_ids()