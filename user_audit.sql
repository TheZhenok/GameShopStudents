CREATE OR REPLACE FUNCTION 
process_user_audit() RETURNS TRIGGER
AS 
$$
DECLARE
    msg TEXT;
BEGIN
    msg = NEW.email || ' ' || NEW.firstname || ' ' || NEW.lastname || ' ' || NEW.wallet;
    IF (TG_OP = 'DELETE') THEN
        INSERT INTO transaction(user_id, description)
            VALUES(NEW.id, 'Delete user: ' || msg);
    ELSIF (TG_OP = 'UPDATE') THEN
        INSERT INTO transaction(user_id, description)
            VALUES(NEW.id, 'Update user: ' || msg);
    ELSIF (TG_OP = 'INSERT') THEN
        INSERT INTO transaction(user_id, description)
            VALUES(NEW.id, 'Insert user: ' || msg);
    END IF;
    RETURN NULL;
END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trigger_user_audit
AFTER INSERT OR UPDATE OR DELETE ON "user" FOR EACH ROW
EXECUTE PROCEDURE process_user_audit();