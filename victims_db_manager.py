import sqlite3


class VictimManager:
    
    def __init__(self):
        ''' Initialize database of victims '''
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS victims
                       (victim_id INTEGER UNIQUE,
                        abuse_type INTEGER,
                        chance INTEGER)''')
        connection.commit()
        connection.close()



    ### Get DB connections
    def get_connection(self):
        ''' Get a victim database connection object '''
        connection = sqlite3.connect('victims')
        return connection


    def retrieve_table(self):
        '''Retrieve the entire victims table'''
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM victims')
        victims = cursor.fetchall()
        connection.close()
        return victims

    def retrieve_just_victims(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT victim_id FROM victims')
        crude_victims = cursor.fetchall()
        victims = [victim[0] for victim in crude_victims]
        connection.close()
        return victims

    def add_new_victim(self,
                       victim_id: int,
                       abuse_type: int,
                       chance: int) -> None:
        ''' Add new victim to be bullied '''
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('''INSERT INTO victims
                            (victim_id, abuse_type, chance)
                            VALUES (?,?,?)''', (victim_id, abuse_type, chance,))
            connection.commit()
            connection.close()
            return f"Successfully added new victim {victim_id}"
        except Exception as e:
            return f"ERROR: User {victim_id} already registered!"

    def liberate_victim(self,
                        victim_id: int):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute('''DELETE FROM victims
                           WHERE victim_id=?
                           ''', (victim_id,))
            connection.commit()
            connection.close()
            return f"Successfully liberated victim {victim_id}"
        except Exception as e:
            return e


    def get_abuse_type_for_victim(self, victim_id):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute('''SELECT abuse_type
                       FROM victims 
                       WHERE victim_id=?''',(victim_id,))
        abuse_type = cursor.fetchone()[0]
        connection.close()
        return abuse_type

    def get_chance_for_victim(self, victim_id):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute('''SELECT chance 
                       FROM victims
                       WHERE victim_id=?''',(victim_id,))
        chance = cursor.fetchone()[0]
        connection.close()
        return chance


    def drop_db(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute('DROP TABLE victims')
        connection.commit()
        connection.close()