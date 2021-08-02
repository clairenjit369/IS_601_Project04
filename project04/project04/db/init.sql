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
    'email' VARCHAR(100) CHARACTER SET utf8,
    primary key(`id`)
);


INSERT INTO addresses (Fname, Lname, Address, City, State, ZipCode, email) VALUES
    ('Isabel','Walters','380 Wilson Lane','Easton','PA', 18042, 'NA'),
    ('Glen','Sanders','88 Manhattan Street','Bloomton','IN', 47401, 'NA'),
    ('Elbert','Hall','85 Pineknoll Drive','Newtown','PA', 18940, 'NA'),
    ('Jason','Hammond','9824 Lakeshore St.','Fleming','FL', 32003, 'NA'),
    ('Paul','Stewart','556 Gartner St.','Westmont','IL', 60559, 'NA'),
    ('Nathan','Mcguire','144 East Bohemia Ave.','Floral','NY', 11001, 'NA'),
    ('Kelli','Pope','89 Fulton Rd.','Des Moines','IA', 50265, 'NA'),
    ('Russel','Caldwell','147 1st Drive','Morrisville','PA',19067, 'NA'),
    ('Julian','Nash','2 S. Thompson Ave.','Gallatin','TN', 37066, 'NA'),
    ('Jennifer','Jordan','371 Holly Avenue','Hartsville','SC', 29550, 'NA'),
    ('Darrin','Brian','7155 Cambridge Court','Pewaukee','WI', 53072, 'NA'),
    ('Dexter','Adkins','7946 Roberts Street','Kalamazoo',' MI', 49009, 'NA'),
    ('Fredrick','Strickland','8639 Lafayette Drive','Lake Charles',' LA', 70605, 'NA'),
    ('Stephanie','Mcdaniel','9163 Union St.','Fargo','ND', 58102, 'NA'),
    ('Jeffrey','Gomez','2 Oak Ave.','Marshalltown','IA', 50158, 'NA'),
    ('Pam','Ryan','9833 SE. Ohio Rd.','New Milford','CT', 06776, 'NA'),
    ('Billie','Hall','853 Corona Ave.','Boca Raton','FL', 33428, 'NA'),
    ('Harold','Mckinney','376 Nut Swamp Dr.','Randolph','MA', 02368, 'NA'),
    ('Muriel','Kim','55 Wild Horse Street','Framingham','MA', 01701, 'NA'),
    ('Alberto','Phillips','624 Rocky River St.','York','PA', 17402, 'NA')
;
