CREATE TABLE "dining_halls" (
	"name"	TEXT,
	PRIMARY KEY("name")
)                                                                                                                                                                                                                                                                                                                                                                                                                                                                        ;

CREATE TABLE "dining_data" (
	"id" TEXT,
	"dining_hall" TEXT,
	"special_data" TEXT,
	"weekly_schedule" TEXT,
	"daily_schedule" TEXT,
	"year" INTEGER,
	"month" INTEGER,
	"day" INTEGER,
	"created_at" TEXT,
	FOREIGN KEY("dining_hall") REFERENCES "dining_halls"("name"),
	PRIMARY KEY("id")
);

CREATE TABLE "dishes" (
	"id"	TEXT,
	"name"	TEXT,
	"description"	TEXT,
	"vegitarian"	INTEGER,
	"station"	TEXT,
	"meal"	TEXT,
	"dining_hall"	TEXT,
	FOREIGN KEY("dining_hall") REFERENCES "dining_halls"("name"),
	PRIMARY KEY("id")
);

CREATE TABLE "laundry_machines" (
	"id"	INTEGER,
	"room_id"	INTEGER NOT NULL,
	"type"	TEXT NOT NULL,
	PRIMARY KEY("id")
);

CREATE TABLE "laundry_rooms" (
	"id"	INTEGER,
	"name"	TEXT NOT NULL,
	PRIMARY KEY("id")
);

CREATE TABLE "auth" (
	"key"	TEXT,
	"name"	TEXT NOT NULL,
	"email"	INTEGER NOT NULL,
	"joined"	TEXT NOT NULL,
	"type"	INTEGER NOT NULL DEFAULT 0,
	"valid"	INTEGER NOT NULL DEFAULT 1,
	PRIMARY KEY("key")
);
