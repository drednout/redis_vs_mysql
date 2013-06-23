ALTER TABLE `weekly_tournament` 
ADD UNIQUE INDEX `complex_key` (`tournament_id` ASC, `person_id` ASC) ;
