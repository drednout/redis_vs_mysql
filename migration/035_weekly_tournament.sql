CREATE  TABLE `weekly_tournament` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `tournament_id` INT NOT NULL COMMENT 'Дата начала турнира' ,
  `person_id` INT NOT NULL COMMENT 'См. persons.id' ,
  `money_earned` INT NOT NULL DEFAULT 0 COMMENT 'Сколько заработано денег в турнире?' ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_bin
COMMENT = 'Таблица для хранения результатов еженедельного турнира';
