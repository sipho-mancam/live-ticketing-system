DELIMITER //
DROP PROCEDURE IF EXISTS populate_tasks_for_tickets;

CREATE PROCEDURE populate_tasks_for_tickets()
BEGIN
    DECLARE counter INT DEFAULT 1;
    DECLARE ticket_description VARCHAR(255);

    -- Start the loop with 8 iterations
    WHILE counter <= 8 DO
        -- Build ticket description
        SET ticket_description = CONCAT('Task 1 for ticket ', CAST(counter AS CHAR));

        -- Populate tasks for the current ticket (using loop index as ticket_id)
        INSERT INTO tasks (description, ticket_id, status, assigned_to, assigned_date)
        VALUES
        (ticket_description, counter, 0, 1, NOW()),
        (CONCAT('Task 2 for ticket ', CAST(counter AS CHAR)), counter, 1, 2, NOW()),
        (CONCAT('Task 3 for ticket ', CAST(counter AS CHAR)), counter, 2, 3, NOW()),
        (CONCAT('Task 4 for ticket ', CAST(counter AS CHAR)), counter, 0, 4, NOW()),
        (CONCAT('Task 5 for ticket ', CAST(counter AS CHAR)), counter, 1, 5, NOW());
        
        -- Increment the counter for the next iteration
        SET counter = counter + 1;
    END WHILE;
END //

DELIMITER ;

-- Call the procedure to start the loop and populate tasks for tickets
CALL populate_tasks_for_tickets();