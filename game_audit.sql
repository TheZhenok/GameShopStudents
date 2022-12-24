CREATE OR REPLACE FUNCTION 
process_game_audit() RETURNS TRIGGER
AS 
$$
DECLARE
    msg TEXT;
BEGIN
    msg = NEW.title || ' ' || NEW.price || ' ' || NEW.count;
    IF (TG_OP = 'DELETE') THEN
        INSERT INTO transaction(game_id, description)
            VALUES(NEW.id, 'Delete game: ' || msg);
    ELSIF (TG_OP = 'UPDATE') THEN
        INSERT INTO transaction(game_id, description)
            VALUES(NEW.id, 'Update game: ' || msg);
    ELSIF (TG_OP = 'INSERT') THEN
        INSERT INTO transaction(game_id, description)
            VALUES(NEW.id, 'Insert game: ' || msg);
    END IF;
    RETURN NULL;
END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trigger_game_audit
AFTER INSERT OR UPDATE OR DELETE ON game FOR EACH ROW
EXECUTE PROCEDURE process_game_audit();