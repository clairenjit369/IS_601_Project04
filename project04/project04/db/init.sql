CREATE DATABASE addressBook;
use addressBook;


CREATE TABLE IF NOT EXISTS addresses (
	`id` int AUTO_INCREMENT,
    `Fname` VARCHAR(20) CHARACTER SET utf8,
    `Lname` VARCHAR(20) CHARACTER SET utf8,
    `Address` VARCHAR(50) CHARACTER SET utf8,
    `City` VARCHAR(50) CHARACTER SET utf8,
    `State` VARCHAR(3) CHARACTER SET utf8,
    `ZipCode` INT,
    primary key(`id`)
);


INSERT INTO addresses (Fname, Lname, Address, City, State, ZipCode) VALUES
    ('Isabel','Walters','380 Wilson Lane','Easton','PA', 18042),
    ('Glen','Sanders','88 Manhattan Street','Bloomton','IN', 47401),
    ('Elbert','Hall','85 Pineknoll Drive','Newtown','PA', 18940),
    ('Jason','Hammond','9824 Lakeshore St.','Fleming','FL', 32003),
    ('Paul','Stewart','556 Gartner St.','Westmont','IL', 60559),
    ('Nathan','Mcguire','144 East Bohemia Ave.','Floral','NY', 11001),
    ('Kelli','Pope','89 Fulton Rd.','Des Moines','IA', 50265),
    ('Russel','Caldwell','147 1st Drive','Morrisville','PA',19067),
    ('Julian','Nash','2 S. Thompson Ave.','Gallatin','TN', 37066),
    ('Jennifer','Jordan','371 Holly Avenue','Hartsville','SC', 29550),
    ('Darrin','Brian','7155 Cambridge Court','Pewaukee','WI', 53072),
    ('Dexter','Adkins','7946 Roberts Street','Kalamazoo',' MI', 49009),
    ('Fredrick','Strickland','8639 Lafayette Drive','Lake Charles',' LA', 70605),
    ('Stephanie','Mcdaniel','9163 Union St.','Fargo','ND', 58102),
    ('Jeffrey','Gomez','2 Oak Ave.','Marshalltown','IA', 50158),
    ('Pam','Ryan','9833 SE. Ohio Rd.','New Milford','CT', 06776),
    ('Billie','Hall','853 Corona Ave.','Boca Raton','FL', 33428),
    ('Harold','Mckinney','376 Nut Swamp Dr.','Randolph','MA', 02368),
    ('Muriel','Kim','55 Wild Horse Street','Framingham','MA', 01701),
    ('Alberto','Phillips','624 Rocky River St.','York','PA', 17402)
;
