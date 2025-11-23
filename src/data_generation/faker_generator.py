"""
Gerador de dados fictícios usando Faker para simular um e-commerce
"""
import os
from datetime import datetime, timedelta
import random
from typing import List, Dict
from faker import Faker
import pandas as pd
from loguru import logger

# Configurar Faker para português do Brasil
fake = Faker('pt_BR')
Faker.seed(42)
random.seed(42)


class EcommerceDataGenerator:
    """Classe para gerar dados fictícios de e-commerce"""
    
    def __init__(self):
        self.fake = fake
        self.categorias = [
            'Eletrônicos', 'Roupas', 'Livros', 'Casa e Decoração',
            'Esportes', 'Brinquedos', 'Beleza', 'Alimentos',
            'Informática', 'Ferramentas'
        ]
        self.status_pedido = ['pendente', 'processando', 'enviado', 'entregue', 'cancelado']
        self.tipos_evento = ['pageview', 'add_to_cart', 'remove_from_cart', 'checkout', 'purchase']
        
    def gerar_clientes(self, num_clientes: int = 10000) -> pd.DataFrame:
        """Gera dados de clientes"""
        logger.info(f"Gerando {num_clientes} clientes...")
        
        clientes = []
        data_inicio = datetime.now() - timedelta(days=365*3)  # 3 anos atrás
        
        for i in range(num_clientes):
            cliente = {
                'id_cliente': i + 1,
                'nome': self.fake.name(),
                'email': self.fake.email(),
                'telefone': self.fake.phone_number(),
                'cpf': self.fake.cpf(),
                'data_nascimento': self.fake.date_of_birth(minimum_age=18, maximum_age=80),
                'endereco': self.fake.street_address(),
                'cidade': self.fake.city(),
                'estado': self.fake.state_abbr(),
                'cep': self.fake.postcode(),
                'data_cadastro': data_inicio + timedelta(days=random.randint(0, 365*3)),
                'ativo': random.choice([True, True, True, False])  # 75% ativo
            }
            clientes.append(cliente)
            
            if (i + 1) % 1000 == 0:
                logger.debug(f"Gerados {i + 1} clientes...")
        
        df = pd.DataFrame(clientes)
        logger.success(f"✓ {num_clientes} clientes gerados com sucesso!")
        return df
    
    def gerar_produtos(self, num_produtos: int = 1000) -> pd.DataFrame:
        """Gera dados de produtos"""
        logger.info(f"Gerando {num_produtos} produtos...")
        
        produtos = []
        
        for i in range(num_produtos):
            categoria = random.choice(self.categorias)
            produto = {
                'id_produto': i + 1,
                'nome_produto': self.fake.catch_phrase(),
                'descricao': self.fake.text(max_nb_chars=200),
                'categoria': categoria,
                'subcategoria': f"{categoria} - {self.fake.word().title()}",
                'preco': round(random.uniform(10.0, 5000.0), 2),
                'custo': round(random.uniform(5.0, 2500.0), 2),
                'estoque': random.randint(0, 1000),
                'fornecedor': self.fake.company(),
                'peso_kg': round(random.uniform(0.1, 50.0), 2),
                'dimensoes': f"{random.randint(10,100)}x{random.randint(10,100)}x{random.randint(5,50)}",
                'ativo': random.choice([True, True, True, False]),
                'data_cadastro': self.fake.date_time_between(start_date='-2y', end_date='now')
            }
            produtos.append(produto)
        
        df = pd.DataFrame(produtos)
        logger.success(f"✓ {num_produtos} produtos gerados com sucesso!")
        return df
    
    def gerar_pedidos(self, num_pedidos: int, clientes_ids: List[int]) -> pd.DataFrame:
        """Gera dados de pedidos"""
        logger.info(f"Gerando {num_pedidos} pedidos...")
        
        pedidos = []
        data_inicio = datetime.now() - timedelta(days=365*2)  # 2 anos atrás
        
        for i in range(num_pedidos):
            data_pedido = data_inicio + timedelta(
                days=random.randint(0, 365*2),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
            
            status = random.choice(self.status_pedido)
            
            pedido = {
                'id_pedido': i + 1,
                'id_cliente': random.choice(clientes_ids),
                'data_pedido': data_pedido,
                'valor_total': 0,  # Será calculado depois com itens
                'valor_frete': round(random.uniform(0, 50.0), 2),
                'valor_desconto': round(random.uniform(0, 100.0), 2),
                'status': status,
                'forma_pagamento': random.choice(['credito', 'debito', 'pix', 'boleto']),
                'parcelas': random.choice([1, 2, 3, 6, 12]),
                'cupom_desconto': self.fake.bothify(text='CUPOM####') if random.random() > 0.7 else None,
                'data_atualizacao': data_pedido + timedelta(days=random.randint(0, 30))
            }
            pedidos.append(pedido)
            
            if (i + 1) % 5000 == 0:
                logger.debug(f"Gerados {i + 1} pedidos...")
        
        df = pd.DataFrame(pedidos)
        logger.success(f"✓ {num_pedidos} pedidos gerados com sucesso!")
        return df
    
    def gerar_itens_pedido(self, pedidos_df: pd.DataFrame, produtos_df: pd.DataFrame) -> pd.DataFrame:
        """Gera itens de pedidos"""
        num_pedidos = len(pedidos_df)
        logger.info(f"Gerando itens para {num_pedidos} pedidos...")
        
        itens = []
        item_id = 1
        
        for _, pedido in pedidos_df.iterrows():
            # Cada pedido tem entre 1 e 5 itens
            num_itens = random.randint(1, 5)
            produtos_selecionados = produtos_df.sample(n=num_itens)
            
            valor_total_pedido = 0
            
            for _, produto in produtos_selecionados.iterrows():
                quantidade = random.randint(1, 3)
                valor_unitario = produto['preco']
                
                item = {
                    'id_item': item_id,
                    'id_pedido': pedido['id_pedido'],
                    'id_produto': produto['id_produto'],
                    'quantidade': quantidade,
                    'valor_unitario': valor_unitario,
                    'valor_total': round(quantidade * valor_unitario, 2),
                    'desconto_item': round(random.uniform(0, 20.0), 2) if random.random() > 0.8 else 0
                }
                itens.append(item)
                valor_total_pedido += item['valor_total']
                item_id += 1
            
            # Atualizar valor total do pedido
            pedidos_df.at[pedido.name, 'valor_total'] = round(valor_total_pedido, 2)
        
        df = pd.DataFrame(itens)
        logger.success(f"✓ {len(itens)} itens de pedido gerados com sucesso!")
        return df, pedidos_df
    
    def gerar_evento_website(self) -> Dict:
        """Gera um único evento de website (para streaming)"""
        evento = {
            'timestamp': datetime.now().isoformat(),
            'id_cliente': random.randint(1, 10000),
            'sessao_id': self.fake.uuid4(),
            'tipo_evento': random.choice(self.tipos_evento),
            'pagina': random.choice([
                '/home', '/produtos', '/carrinho', '/checkout',
                '/produto/123', '/categoria/eletronicos', '/minha-conta'
            ]),
            'dispositivo': random.choice(['desktop', 'mobile', 'tablet']),
            'navegador': random.choice(['Chrome', 'Firefox', 'Safari', 'Edge']),
            'sistema_operacional': random.choice(['Windows', 'MacOS', 'Linux', 'iOS', 'Android']),
            'ip': self.fake.ipv4(),
            'pais': 'Brasil',
            'cidade': self.fake.city(),
            'referrer': random.choice([
                'google.com', 'facebook.com', 'instagram.com',
                'direct', 'email', None
            ])
        }
        return evento


def main():
    """Função principal para testar a geração de dados"""
    logger.info("Iniciando geração de dados fictícios...")
    
    generator = EcommerceDataGenerator()
    
    # Gerar dados
    clientes_df = generator.gerar_clientes(100)
    produtos_df = generator.gerar_produtos(50)
    pedidos_df = generator.gerar_pedidos(200, clientes_df['id_cliente'].tolist())
    itens_df, pedidos_df = generator.gerar_itens_pedido(pedidos_df, produtos_df)
    
    # Mostrar amostras
    logger.info("\n=== AMOSTRA DE CLIENTES ===")
    print(clientes_df.head())
    
    logger.info("\n=== AMOSTRA DE PRODUTOS ===")
    print(produtos_df.head())
    
    logger.info("\n=== AMOSTRA DE PEDIDOS ===")
    print(pedidos_df.head())
    
    logger.info("\n=== AMOSTRA DE ITENS ===")
    print(itens_df.head())
    
    # Gerar evento de website
    logger.info("\n=== EVENTO DE WEBSITE ===")
    evento = generator.gerar_evento_website()
    print(evento)
    
    logger.success("✓ Geração de dados concluída com sucesso!")


if __name__ == "__main__":
    main()