from neo4j import GraphDatabase
from settings import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD


class Neo4jClient:
    def __init__(self):

        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    def close(self):
        self.driver.close()

    def query(self, query, **kwargs):
        with self.driver.session() as session:
            session.run(query, **kwargs)

    def query_data_response(self, query, **kwargs):
        with self.driver.session() as session:
            result =  session.run(query, **kwargs)
            data = result.data()  # Metoda 'data()' zwraca wszystkie wyniki jako listę słowników
            return data

    def fetch_all_data(self):
        with self.driver.session() as session:
            # Wykonujemy zapytanie, które zwróci wszystkie węzły
            result = session.run("MATCH (n) RETURN n LIMIT 25")  # Zmieniaj LIMIT wg potrzeb
            for record in result:
                pass
                # print(record["n"])

    # def query_single(self, query, **kwargs):
    #     with self.driver.session() as session:
    #         return session.run(query, **kwargs).single()
    #
    # def query_list(self, query, **kwargs):
    #     with self.driver.session() as session:
    #         return session.run(query, **kwargs).data()
    #
    # def query_value(self, query, **kwargs):
    #     with self.driver.session() as session:
    #         return session.run(query, **kwargs).single().value()
    #
    # def query_values(self, query, **kwargs):
    #     with self.driver.session() as session:
    #         return [record.value() for record in session.run(query, **kwargs)]
    #
    # def query_dict(self, query, **kwargs):
    #     with self.driver.session() as session:
    #         return session.run(query, **kwargs).single().data()
    #
    # def query_dicts(self, query, **kwargs):
    #     with self.driver.session() as session:
    #         return [record.data() for record in session.run(query, **kwargs)]
    #
    # def query_table(self, query, **kwargs):
    #     with self.driver.session() as session:
    #         return session.run(query, **kwargs).to_table()
    #
    # def query_plan(self, query, **kwargs):
    #     with self.driver.session() as session:
    #         return session.run(query, **kwargs).explain()
    #
    # def query_profile(self, query, **kwargs):
    #     with self.driver.session() as session:
    #         return session.run(query, **kwargs).profile()
    #
    # def query_summary(self, query, **kwargs):
    #     with self.driver.session() as session:
    #         return session.run(query, **kwargs).summary()
    #
    # def query_read_transaction(self, query, **kwargs):
    #     with self.driver.session() as session:
    #         return session.read_transaction(query, **kwargs)
    #
    # def query_write_transaction(self, query, **kwargs):
    #     with self.driver.session() as session:
    #         return session.write_transaction(query, **kwargs)
    #
    # def query_read_transaction_single(self, query, **kwargs):
    #     with self.driver.session() as session:
    #         return session.read_transaction(query, **kwargs).single()

