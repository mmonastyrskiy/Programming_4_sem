from dbtable import *
class RoomTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + "Room"

    def columns(self):
        return {"person_id": ["integer", "REFERENCES people(id)"],
                "phone": ["varchar(12)", "NOT NULL"]}


{
    "id":["integer","PRIMARY KEY"],
    "name": ["character varying(50)", "NOT NULL"],
    "space": ["numeric(7,2)", "NOT NULL"],
    "space_left":["numeric(7,2)", "NOT NULL"],
    "min_humidity":["numeric(8,2)","NOT NULL"],
    "max_humidity":["numeric(8,2)" ,"NOT NULL"],
    "min_temp": ["numeric(5,2)", "NOT NULL"],
    "max_temp":["numeric(5,2)","NOT NULL"]
    CONSTRAINT uni_room_name UNIQUE (name),
	CONSTRAINT positive_volume_left_room CHECK(space_left >0),
	CONSTRAINT positive_volume_room CHECK(space >0),
	CONSTRAINT volume_left_le_volume CHECK(space_left <= space),
	CONSTRAINT hu_max_in_interval CHECK (max_humidity <= 100 and max_humidity >= 0),
	CONSTRAINT hu_min_in_interval CHECK (min_humidity <= 100 and min_humidity >= 0)
	}

