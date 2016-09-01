from peewee import *
from math import cos, sin, pi

database = SqliteDatabase('sgData.db')

class UnknownField(object):
    pass

class BaseModel(Model):
    class Meta:
        database = database

class BusStop(BaseModel):
    BusStopCode = CharField(db_column='BusStopCode', null=True, unique=True, primary_key=True)
    Description = TextField(db_column='Description', null=True)
    Latitude = DecimalField(db_column='Latitude', null=True)
    Longitude = DecimalField(db_column='Longitude', null=True)
    RoadName = TextField(db_column='RoadName', null=True)

    class Meta:
        db_table = 'BusStop'

class BusServices(BaseModel):
    ServiceNo = CharField()
    Operator = CharField()
    Direction = CharField()
    Category = CharField()
    OriginCode = CharField()
    DestinationCode = CharField()
    AM_Peak_Freq = CharField()
    AM_Offpeak_Freq = CharField()
    PM_Peak_Freq = CharField()
    PM_Offpeak_Freq = CharField()
    LoopDesc = TextField()

    class Meta:
        db_table = 'BusServices'
        primary_key = CompositeKey('ServiceNo', 'Direction')

class BusRoutes(BaseModel):
    ServiceNo = CharField()
    Operator = CharField(null=True)
    Direction = CharField(null=True)
    StopSequence = IntegerField(null=True)
    BusStopCode = CharField(null=True)
    Distance = CharField(null=True)
    WD_FirstBus = CharField(null=True)
    WD_LastBus = CharField(null=True)
    SAT_FirstBus = CharField(null=True)
    SAT_LastBus = CharField(null=True)
    SUN_FirstBus = CharField(null=True)
    SUN_LastBus = CharField(null=True)

    class Meta:
        db_table = 'BusRoutes'
        primary_key = CompositeKey('ServiceNo', 'Direction', 'BusStopCode', 'StopSequence')

class TaxiAvailability(BaseModel):
    id = PrimaryKeyField()
    Latitude = DecimalField(db_column='Latitude', null=True)
    Longitude = DecimalField(db_column='Longitude', null=True)
    cos_lat = FloatField(null=True)
    sin_lat = FloatField(null=True)
    cos_lng = FloatField(null=True)
    sin_lng = FloatField(null=True)

    class Meta:
        db_table = 'TaxiAvailability'

class sgDataBL(object):
    def __init__(self):
        database.connect()
        database.create_tables([BusStop, BusServices, BusRoutes, TaxiAvailability], safe=True)

    def atomic(self):
        return database.atomic()

    def close(self):
        database.close()

    ##### BusStop Table - Start #####
    def get_busstop(self, BusStopID):
        return BusStop.select().where(BusStop.BusStopCode == BusStopID)
    
    def clear_busstops(self):
        q = BusStop.delete()
        q.execute()

    def add_busstops(self, rows):
        BusStop.insert_many(rows).execute()        

    def add_busstop(self, BusStopCode, RoadName, Description, Latitude, Longitude):
        try:
            BusStop.create(BusStopCode=BusStopCode, RoadName=RoadName, Description=Description, Latitude=Latitude, Longitude=Longitude)
        except IntegrityError:
            raise ValueError("Data already exists.")
    ##### BusStop Table - Stop #####

    ##### BusServices Table - Start #####
    def get_busservices(self, ServiceNo):
        return BusServices.select().where(BusServices.ServiceNo == ServiceNo)

    def clear_busservices(self):
        q = BusServices.delete()
        q.execute()

    def add_busservices(self, rows):
        BusServices.insert_many(rows).execute()
    ##### BusServices Table - Stop #####

    ##### BusRoutes Table - Start #####
    def get_busroutes(self, ServiceNo):
        return BusRoutes.select().where(BusRoutes.ServiceNo == ServiceNo)

    def clear_busroutes(self):
        q = BusRoutes.delete()
        q.execute()

    def add_busroutes(self, rows):
        BusRoutes.insert_many(rows).execute()
    ##### BusRoutes Table - Stop #####

    ##### TaxiAvailability Table - Start #####
    def get_taxiavailability(self, Latitude, Longitude, Radius):
        cur_cos_lat = cos(Latitude * pi / 180)
        cur_sin_lat = sin(Latitude * pi / 180)
        cur_cos_lng = cos(Longitude * pi / 180)
        cur_sin_lng = sin(Longitude * pi / 180)
        cos_allowed_distance = cos(Radius / 6371)
        return TaxiAvailability.select().where(cur_sin_lat * TaxiAvailability.sin_lat + cur_cos_lat * TaxiAvailability.cos_lat * (TaxiAvailability.cos_lng * cur_cos_lng + TaxiAvailability.sin_lng * cur_sin_lng) > cos_allowed_distance)
    
    def clear_taxiavailability(self):
        q = TaxiAvailability.delete()
        q.execute()

    def add_taxiavailability(self, rows):
        TaxiAvailability.insert_many(rows).execute()

    def add_taxiavailabilitysingle(self, Latitude, Longitude, cos_lat, sin_lat, cos_lng, sin_lng):
        try:
            TaxiAvailability.create(Latitude=Latitude, Longitude=Longitude, cos_lat=cos_lat, sin_lat=sin_lat, cos_lng=cos_lng, sin_lng=sin_lng)
        except IntegrityError:
            raise ValueError("Data already exists.")
    ##### TaxiAvailability Table - Stop #####
