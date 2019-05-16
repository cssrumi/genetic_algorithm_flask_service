import sys
import os

sys.path.append(os.path.abspath("../"))
sys.path.append(os.path.join(os.path.abspath("../"), 'genetic_algorithm'))


class TestDataObject:
    def __init__(self):
        self.Czas_Pomiaru = 123
        self.PmGdaPoWie01_PM10_1g = 5123
        self.Kierunek_wiatru = 666
        self.Predkosc_wiatru = 23
        self.Temperatura_powietrza = 654
        self.Wilgotnosc = 879
        self.Temperatura_punktu_rosy = 1
        self.Cisnienie = 2


map_object = TestDataObject()

default_key_dict = {
    'date_time': 'Czas_Pomiaru',
    'pm10': 'PmGdaPoWie01_PM10_1g',
    'wind_direction': 'Kierunek_wiatru',
    'wind': 'Predkosc_wiatru',
    'temperature': 'Temperatura_powietrza',
    'humidity': 'Wilgotnosc',
    'dew_point': 'Temperatura_punktu_rosy',
    'pressure': 'Cisnienie',
}


def data_mapper_test():
    from data.data_mapper import DataMapper

    try:
        dm = DataMapper(default_key_dict)
        data = dm.get_data_object(map_object)
        print(data)
    except Exception as e:
        print(e)
    print('DataMapper test completed')


def training_data_test():
    from data.data_mapper import DataMapper
    from data.training_data import TrainingData

    try:
        dm = DataMapper(default_key_dict)
        data = dm.get_data_object(map_object)

        td = TrainingData(data, pm10_after_24h=1111)
        print(td)
    except Exception as e:
        print(e)
    print('TrainingData test completed')


def mongodb_test():
    from data.data_connector import DataConnectorFactory
    from data.data_mapper import DataMapper
    from data.db.db_param import DBParam
    import os

    db_type = 'mongodb'
    dm = DataMapper(DataMapper.get_default_mapping())
    print(DataMapper.get_default_mapping())
    MongoDB = DataConnectorFactory.get_data_connector(db_type)
    mongodb_param = DBParam(
        ip=os.getenv('DATA_CONNECTOR_IP', '192.168.0.59'),
        port=os.getenv('DATA_CONNECTOR_PORT', '27018'),
        user=os.getenv('DATA_CONNECTOR_USER', 'root'),
        password=os.getenv('DATA_CONNECTOR_PASSWORD', 'example'),
        db_name=os.getenv('DATABASE_NAME', 'data'),
        table_name=os.getenv('TABLE_NAME', 'data'),
    )
    mongo = MongoDB(mongodb_param, dm)
    mongo.connect()
    data = mongo.get_data(1)
    print(data)
    print('MongoDB test completed')


def sql_model_test():
    from data.data_connector import DataConnectorFactory
    from data.data_mapper import DataMapper
    from data.db.model.data_sql_model import SQLData
    from data.db.db_param import DBParam
    import os

    db_type = 'mysql'
    dm = DataMapper(DataMapper.get_default_mapping())
    MySQL = DataConnectorFactory.get_data_connector(db_type)
    mysql_param = DBParam(
        ip=os.getenv('DATA_CONNECTOR_IP', '192.168.0.59'),
        port=os.getenv('DATA_CONNECTOR_PORT', '3306'),
        user=os.getenv('DATA_CONNECTOR_USER', 'root'),
        password=os.getenv('DATA_CONNECTOR_PASSWORD', 'example'),
        db_name=os.getenv('DATABASE_NAME', 'data'),
        table_name=os.getenv('TABLE_NAME', 'data'),
    )
    mysql = MySQL(mysql_param, dm)
    mysql.connect()
    d1 = SQLData(
        date_time=2, pm10=2, wind_direction=3, wind=4,
        temperature=5, humidity=6, dew_point=7, pressure=8
    )
    # mysql.session.add(d1)
    # mysql.session.commit()
    data = mysql.get_data('ALL')
    for d in data:
        print(d)
    print(len(data))

    print('DataSqlModel test completed')


def bootstrap_mysql_test():
    from data.bootstrap.bootstrap import export_data_from_csv, get_abs_path
    from data.data_connector import DataConnectorFactory
    from data.data_mapper import DataMapper
    from data.db.db_param import DBParam
    import os

    db_type = 'mysql'
    dm = DataMapper(DataMapper.get_default_mapping())
    MySQL = DataConnectorFactory.get_data_connector(db_type)
    mysql_param = DBParam(
        ip=os.getenv('DATA_CONNECTOR_IP', '192.168.0.59'),
        port=os.getenv('DATA_CONNECTOR_PORT', '3306'),
        user=os.getenv('DATA_CONNECTOR_USER', 'root'),
        password=os.getenv('DATA_CONNECTOR_PASSWORD', 'example'),
        db_name=os.getenv('DATABASE_NAME', 'data'),
        table_name=os.getenv('TABLE_NAME', 'data'),
    )
    mysql = MySQL(mysql_param, dm)
    mysql.connect()
    csv_file = 'gdansk_2018.csv'
    csv_file = get_abs_path(csv_file)
    export_data_from_csv(csv_file, mysql)


def bootstrap_mssql_test():
    from data.bootstrap.bootstrap import export_data_from_csv, get_abs_path
    from data.data_connector import DataConnectorFactory
    from data.data_mapper import DataMapper
    from data.db.db_param import DBParam
    import os

    db_type = 'mssql'
    dm = DataMapper(DataMapper.get_default_mapping())
    MSSQL = DataConnectorFactory.get_data_connector(db_type)
    mssql_param = DBParam(
        ip=os.getenv('DATA_CONNECTOR_IP', '192.168.0.59'),
        port=os.getenv('DATA_CONNECTOR_PORT', '1433'),
        user=os.getenv('DATA_CONNECTOR_USER', 'sa'),
        password=os.getenv('DATA_CONNECTOR_PASSWORD', '!mssqlAdmin123'),
        db_name=os.getenv('DATABASE_NAME', 'data'),
        table_name=os.getenv('TABLE_NAME', 'data'),
    )
    mssql = MSSQL(mssql_param, dm)
    mssql.connect()
    csv_file = 'gdansk_2018.csv'
    csv_file = get_abs_path(csv_file)
    export_data_from_csv(csv_file, mssql)


def bootstrap_mongodb_test():
    from data.bootstrap.bootstrap import export_data_from_csv, get_abs_path
    from data.data_connector import DataConnectorFactory
    from data.data_mapper import DataMapper
    from data.db.db_param import DBParam
    import os

    db_type = 'mongodb'
    dm = DataMapper(DataMapper.get_default_mapping())
    MongoDB = DataConnectorFactory.get_data_connector(db_type)
    mongodb_param = DBParam(
        ip=os.getenv('DATA_CONNECTOR_IP', '10.111.120.18'),
        port=os.getenv('DATA_CONNECTOR_PORT', '27017'),
        user=os.getenv('DATA_CONNECTOR_USER', 'root'),
        password=os.getenv('DATA_CONNECTOR_PASSWORD', 'example'),
        db_name=os.getenv('DATABASE_NAME', 'data'),
        table_name=os.getenv('TABLE_NAME', 'data'),
    )
    mongodb = MongoDB(mongodb_param, dm)
    mongodb.connect()
    csv_file = 'gdansk_2018.csv'
    csv_file = get_abs_path(csv_file)
    export_data_from_csv(csv_file, mongodb)


def training_data_test():
    from data.data_connector import DataConnectorFactory
    from data.data_mapper import DataMapper
    from data.db.db_param import DBParam
    from data.training_data import create_training_data
    import os

    db_type = 'mysql'
    dm = DataMapper(DataMapper.get_default_mapping())
    MySQL = DataConnectorFactory.get_data_connector(db_type)
    mysql_param = DBParam(
        ip=os.getenv('DATA_CONNECTOR_IP', '192.168.0.59'),
        port=os.getenv('DATA_CONNECTOR_PORT', '3306'),
        user=os.getenv('DATA_CONNECTOR_USER', 'root'),
        password=os.getenv('DATA_CONNECTOR_PASSWORD', 'example'),
        db_name=os.getenv('DATABASE_NAME', 'data'),
        table_name=os.getenv('TABLE_NAME', 'data'),
    )
    mysql = MySQL(mysql_param, dm)
    mysql.connect()
    data = mysql.get_data('ALL')
    training_data = create_training_data(data)
    print(training_data[0])
    print('MYSQL COMPLETED')
    db_type = 'mssql'

    MSSQL = DataConnectorFactory.get_data_connector(db_type)
    mssql_param = DBParam(
        ip=os.getenv('DATA_CONNECTOR_IP', '192.168.0.59'),
        port=os.getenv('DATA_CONNECTOR_PORT', '1433'),
        user=os.getenv('DATA_CONNECTOR_USER', 'sa'),
        password=os.getenv('DATA_CONNECTOR_PASSWORD', '!mssqlAdmin123'),
        db_name=os.getenv('DATABASE_NAME', 'data'),
        table_name=os.getenv('TABLE_NAME', 'data'),
    )
    mssql = MSSQL(mssql_param, dm)
    mssql.connect()
    data = mssql.get_data('all')
    training_data = create_training_data(data)
    print(training_data[0])
    print('MSSQL COMPLETED')

    db_type = 'mongodb'
    MongoDB = DataConnectorFactory.get_data_connector(db_type)
    mongodb_param = DBParam(
        ip=os.getenv('DATA_CONNECTOR_IP', '192.168.0.59'),
        port=os.getenv('DATA_CONNECTOR_PORT', '27018'),
        user=os.getenv('DATA_CONNECTOR_USER', 'root'),
        password=os.getenv('DATA_CONNECTOR_PASSWORD', 'example'),
        db_name=os.getenv('DATABASE_NAME', 'data'),
        table_name=os.getenv('TABLE_NAME', 'data'),
    )
    mongodb = MongoDB(mongodb_param, dm)
    mongodb.connect()
    data = mongodb.get_data('all')
    training_data = create_training_data(data)
    print(training_data[0])
    print('MONGODB COMPLETED')


def genotype_test():
    from genetic_algorithm.genotype import Genotype
    print(Genotype.gen_list)
    g = Genotype.get_random_genotype()
    print(g)


def phenotype_test():
    from genetic_algorithm.phenotype import Phenotype
    p1 = Phenotype()
    p1.vitality -= 1
    assert Phenotype.VITALITY is not p1.vitality, "shallow copy"
    print(Phenotype.VITALITY, p1.vitality)

    p2 = Phenotype()
    p3 = p1.crossover(p2)
    print(p1)
    print(p2)
    print(p3)


def genetic_algorithm_impl_test():
    from genetic_algorithm.genetic_algorithm_impl import GeneticAlgorithmImpl
    from genetic_algorithm.phenotype import Phenotype
    from data.data_connector import DataConnectorFactory
    from data.data_mapper import DataMapper
    from data.db.db_param import DBParam
    import os

    db_type = 'mongodb'
    dm = DataMapper(DataMapper.get_default_mapping())
    MongoDB = DataConnectorFactory.get_data_connector(db_type)
    mongodb_param = DBParam(
        ip=os.getenv('DATA_CONNECTOR_IP', '192.168.0.59'),
        port=os.getenv('DATA_CONNECTOR_PORT', '27018'),
        user=os.getenv('DATA_CONNECTOR_USER', 'root'),
        password=os.getenv('DATA_CONNECTOR_PASSWORD', 'example'),
        db_name=os.getenv('DATABASE_NAME', 'data'),
        table_name=os.getenv('TABLE_NAME', 'data'),
    )
    mongodb = MongoDB(mongodb_param, dm)
    mongodb.connect()

    g = GeneticAlgorithmImpl(mongodb, 100, 1)
    population = [Phenotype() for _ in range(100)]
    g.population._calculate_fitness(population)
    print(g.population.get_best())
    q = GeneticAlgorithmImpl(mongodb, 100, 1)
    q.population._calculate_fitness_in_parallel(population)
    print(q.population.get_best())
    # g.calculate_fitness_in_parallel_old()
    # for p in g.population:
    #     print(p)


def data_cy_test():
    from genetic_algorithm.data_cy import CyData

    d1 = CyData(0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1)
    print(d1)
    print(d1.temperature)


def genotype_cy_test():
    from genetic_algorithm.genotype_cy import CyGenotype as Genotype

    g1 = Genotype(0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1)
    g2 = Genotype.get_random_genotype()
    print(g1)
    print(g2)


def phenotype_cy_test():
    from genetic_algorithm.phenotype_cy import CyPhenotype, Phenotype

    p1 = Phenotype()
    # p1.
    print(p1)


if __name__ == '__main__':
    # data_mapper_test()
    # training_data_test()
    # mongodb_test()
    # sql_model_test()
    # bootstrap_mysql_test()
    # bootstrap_mssql_test()
    # bootstrap_mongodb_test()
    # training_data_test()
    genotype_test()
    # phenotype_test()
    # genetic_algorithm_impl_test()
    # data_cy_test()
    # genotype_cy_test()
    # phenotype_cy_test()
