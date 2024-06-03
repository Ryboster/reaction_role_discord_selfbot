import sqlite3


class ReactionRoleManager:
    
    def __init__(self):
        ''' Initialize database by creating tables '''
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS watched_messages
                       (message_id INTEGER PRIMARY KEY UNIQUE,
                       channel_id INTEGER);''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS reaction_role
                       (message_id INTEGER,
                       reaction TEXT,
                       role TEXT,
                       FOREIGN KEY (message_id) REFERENCES watched_messages(message_id));''')
        connection.commit()
        connection.close()

    def get_connection(self):
        ''' Get a database connection object '''
        connection = sqlite3.connect('react_role_messages.db')
        return connection
    
    def retrieve_reaction_roles(self):
        ''' Retrieve all values
        from reaction_role table'''
        
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM reaction_role')
        reaction_roles = cursor.fetchall()
        connection.close()
        return reaction_roles

    def retrieve_messages(self):
        ''' Retrieve all values 
        from watched_messages table '''
        
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute('''SELECT * FROM watched_messages''')
        watched_messages = cursor.fetchall()
        connection.close()
        return watched_messages


    def drop_db(self):
        ''' Drop all tables '''
        
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute('''DROP TABLE reaction_role;''')
        cursor.execute('''DROP TABLE watched_messages;''')
        connection.commit()
        connection.close()


    def register_new_watched_message(self,message_id, channel_id):
        ''' Add new watched message
        to watched_messages table '''
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('''INSERT INTO watched_messages 
                           (message_id, channel_id)
                           VALUES (?,?)''',(message_id,channel_id,))
        except Exception as e:
            cursor.execute('''SELECT message_id FROM watched_messages
                           WHERE message_id=?''',(message_id,))
        connection.commit()
        connection.close()


    def add_new_reaction_role(self,reaction, role, message_id):
        ''' Add new reaction role pair
        to reaction_role table'''
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute('''INSERT INTO reaction_role
                        (message_id, reaction, role)
                        VALUES (?,?,?)
                        ''',(message_id, reaction, role))

        connection.commit()
        connection.close()
        
    
