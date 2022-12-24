CREATE OR REPLACE FUNCTION 
process_gamecode_audit() RETURNS TRIGGER
AS 
$$
DECLARE
    msg TEXT;
BEGIN
    msg = NEW.code;
    IF (TG_OP = 'DELETE') THEN
        INSERT INTO transaction(gamecode_id, description)
            VALUES(NEW.id, 'Delete gamecode: ' || msg);
    ELSIF (TG_OP = 'UPDATE') THEN
        INSERT INTO transaction(gamecode_id, description)
            VALUES(NEW.id, 'Update gamecode: ' || msg);
    ELSIF (TG_OP = 'INSERT') THEN
        INSERT INTO transaction(gamecode_id, description)
            VALUES(NEW.id, 'Insert gamecode: ' || msg);
    END IF;
    RETURN NULL;
END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trigger_gamecode_audit
AFTER INSERT OR UPDATE OR DELETE ON game_code FOR EACH ROW
EXECUTE PROCEDURE process_gamecode_audit();