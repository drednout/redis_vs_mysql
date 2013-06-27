ALTER TABLE `weekly_tournament` 
ADD INDEX `money_earned_key` (`tournament_id` DESC, `money_earned` DESC) ;
