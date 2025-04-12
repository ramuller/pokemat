DROP DATABASE pokemat;
CREATE DATABASE IF NOT EXISTS pokemat;
USE pokemat;

CREATE TABLE IF NOT EXISTS  trainers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name CHAR(32) NOT NULL UNIQUE COLLATE utf8_general_ci,
    trainer_code CHAR(14) NOT NULL UNIQUE COLLATE utf8_general_ci,
    team ENUM('red', 'yellow', 'blue') NOT NULL,
    comment CHAR(255),
    first_date DATE NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE IF NOT EXISTS  friends (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name CHAR(32) NOT NULL COLLATE utf8_general_ci,
    trainer CHAR(32) NOT NULL COLLATE utf8_general_ci,
	keep BOOLEAN DEFAULT FALSE,
    trainer_code CHAR(16) UNIQUE COLLATE utf8_general_ci,
    FOREIGN KEY (trainer) REFERENCES trainers(name),
    team ENUM('red', 'yellow', 'blue'),
    first_date DATE NOT NULL DEFAULT CURRENT_DATE,
    last_check DATE NOT NULL DEFAULT CURRENT_DATE,
    last_received DATE NOT NULL DEFAULT CURRENT_DATE,
	has_gift BOOLEAN,
    last_send DATE NOT NULL DEFAULT CURRENT_DATE,
	can_receive BOOLEAN,
    days_to_go BOOLEAN,
    friend_level CHAR(32),
    comment CHAR(255),
    UNIQUE (name, trainer)
);
# CONSTRAINT check_days CHECK (friendlevel <= 4);
INSERT INTO trainers (name, team, trainer_code) VALUE ("aphextvin", "red", "2671 5362 7329");
INSERT INTO trainers (name, team, trainer_code) VALUE ("pokeralle123", "yellow", "6114 6158 2235");
INSERT INTO trainers (name, team, trainer_code) VALUE ("higimmi222", "yellow", "4410 2896 2317");
INSERT INTO trainers (name, team, trainer_code) VALUE ("Yellowthatsit", "yellow", "0908 2008 8686");
INSERT INTO trainers (name, team, trainer_code) VALUE ("higimmi444", "blue", "1512 5107 1002");
INSERT INTO trainers (name, team, trainer_code) VALUE ("blond2023", "yellow", "2430 5402 4528");


INSERT INTO trainers (name, team, trainer_code) VALUE ("schlumpiz", "red", "6054 6366 9708");
INSERT INTO trainers (name, team, trainer_code) VALUE ("localhost", "red", "3617 4276 1937");
INSERT INTO trainers (name, team, trainer_code) VALUE ("plasticgirl", "yellow", "7071 2099 8261");

INSERT INTO trainers (name, team, trainer_code) VALUE ("helmut kaali", "blue","9599 1796 1593");
INSERT INTO trainers (name, team, trainer_code) VALUE ("eizu123", "blue", "3040 7450 1791");

INSERT INTO friends (name, trainer, team, keep) VALUE ("Helmut Kaali", "aphextvin", "blue", TRUE);
