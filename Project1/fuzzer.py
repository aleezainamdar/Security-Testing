from fuzzingbook.GrammarFuzzer import EvenFasterGrammarFuzzer
from fuzzingbook.ProbabilisticGrammarFuzzer import ProbabilisticGrammarFuzzer
import grammar
import random
import re
import string


def generate_random_string(length):
    # Generate a random string of the specified length
    return ''.join(random.choice(string.ascii_letters) for _ in range(1,length))


class Fuzzer:
    def __init__(self):
        # This function must not be changed.
        self.grammar = grammar.grammar
        self.setup_fuzzer()
        self.tables = {}
        self.indexs = []
        self.views = []
        self.triggers = []
        self.savepoints = []
        self.attached_db = {}

    def setup_fuzzer(self):
        # This function may be changed.
        self.fuzzer = ProbabilisticGrammarFuzzer(self.grammar)

    def fuzz_one_input(self) -> str:
        while True:
            sql_command = self.fuzzer.fuzz()
            try:
                sql_command = self.parse_command(sql_command)
                break
            except Exception as e:
                continue
        return sql_command

    def create_helper(self,command):
        command_array = command.split()
        if command_array[1] == 'TABLE' and 'SELECT' in command:
            command = ' '.join(command_array)
            s1, s2 = command.split('SELECT', 1)
            s2 = 'SELECT' + s2
            updated_nested_select = self.select_helper(s2)
            updated_command = s1 + updated_nested_select
            updated_command_array = updated_command.split()

            if '*' in updated_command:
                col_index = updated_command_array.index('FROM') + 1
                self.tables[updated_command_array[2]] = self.tables[updated_command_array[col_index]]
            else:
                col_index = updated_command_array.index('SELECT') + 1
                if ',' in updated_command_array[col_index]:
                    cols = updated_command_array[col_index].split(',')
                    self.tables[updated_command_array[2]] = cols
                else:
                    self.tables[updated_command_array[2]] = updated_command_array[col_index]
            return ' '.join(updated_command_array)

        elif "TEMP" in command or "TEMPORARY" in command:
            pattern = re.compile(r'\((.*?)\)')
            match = re.search(pattern, command)
            if "IF NOT EXISTS" in command:
                self.tables[command_array[6]] = match.group(1).split(',')
            self.tables[command_array[3]] = match.group(1).split(',')
            return ' '.join(command_array)

        elif command_array[1] == 'TABLE' and command.count('PRIMARY KEY') <= 1:
            pattern = re.compile(r'\((.*?)\)')
            match = re.search(pattern, command)
            self.tables[command_array[2]] = match.group(1).split(',')
            return ' '.join(command_array)

        elif 'INDEX' in command:
            index_pos = 2
            table_pos = 4
            if 'UNIQUE' in command:
                index_pos = 3
                table_pos = 5
            # Choose random index name
            command_array[index_pos] = generate_random_string(5)
            # while random_name in self.indexs:
            #    command_array[index_pos] = generate_random_string(5)
            # Choose random table name
            random_table_name = random.choice(list(self.tables.keys()))
            # while random_table_name == command_array[index_pos]:
            #    random_table_name = random.choice(list(self.tables.keys()))
            pattern = re.compile(r'\([^)]*\)')
            replacement = ','.join(self.tables[random_table_name])
            updated_command = re.sub(pattern, f'({replacement})', command)
            c = updated_command.split()
            c[table_pos] = random_table_name
            self.indexs.append(c[index_pos])
            return ' '.join(c)

        elif command_array[1] == 'VIEW':
            # Choose random view name
            if command_array[2] in self.views:
                command_array[2] = generate_random_string(5)
            self.views.append(command_array[2])
            command = ' '.join(command_array)
            if 'SELECT' in command:
                s1, s2 = command.split('SELECT', 1)
                s2 = 'SELECT' + s2
                updated_nested_select = self.select_helper(s2)
            return s1 + updated_nested_select


        elif command_array[1] == 'TRIGGER':
            n = 6
            if 'INSTEAD OF' in command:
                n = 7
            # Choose random trigger name
            random_name = generate_random_string(5)
            if random_name in self.triggers:
                command_array[2] = generate_random_string(5)
            # Choose random table name
            random_table_name = random.choice(list(self.tables.keys()))
            command_array[n] = random_table_name
            self.triggers.append(command_array[2])
            return ' '.join(command_array)

    def drop_helper(self,command):
        command_array = command.split()
        if command_array[1] == 'TABLE' and self.tables != {}:
            random_table_name = random.choice(list(self.tables.keys()))
            command_array[2] = random_table_name
            del self.tables[command_array[2]]
        elif command_array[1] == 'VIEW' and self.views != []:
            random_view_name = random.choice(self.views)
            command_array[2] = random_view_name
            self.views.remove(command_array[2])
        elif command_array[1] == 'TRIGGER' and self.triggers != []:
            random_trigger_name = random.choice(self.triggers)
            command_array[2] = random_trigger_name
            self.triggers.remove(command_array[2])
        elif command_array[1] == 'INDEX' and self.indexs != []:
            random_index_name = random.choice(self.indexs)
            command_array[2] = random_index_name
            self.indexs.remove(command_array[2])
        return ' '.join(command_array)

    def insert_replace_helper(self,command):
        pattern = re.compile(r'\((.*?)\)')
        command_array = command.split()
        random_table_name = random.choice(list(self.tables.keys()))
        command_array[2] = random_table_name
        table_cols = self.tables[command_array[2]]
        if 'SELECT' in command:
            s1, s2 = command.split('SELECT', 1)
            s2 = 'SELECT' + s2
            updated_nested_select = self.select_helper(s2)
            return s1 + updated_nested_select
        values = []
        x = generate_random_string(6)
        for i in table_cols:
            if 'NUM' in i:
                values.append(random.uniform(1.0, 100.0))
            elif 'INT' in i:
                values.append(random.randint(1, 1000))
            elif 'TEXT' in i:
                values.append("'" + x + "'")
            else:
                values.append("'" + x + "'")
        values_string = ', '.join(map(str, values))
        if '(' not in command:
            return ' '.join(command_array)

        elif command.count('(') <= 1:
            updated_command = ' '.join(command_array)
            updated_command = re.sub(pattern, f'({values_string})', updated_command, count=1)
            return updated_command

        else:
            if command.count('(') > 1:
                cols = []
                for i in table_cols:
                    if ' ' in i:
                        col_name = i[:i.index(' ')]
                        cols.append(col_name)
                    else:
                        col_name = i[:i.index(',')]
                        cols.append(col_name)
                cols_string = ','.join(cols)
            updated_command = ' '.join(command_array)
            updated_command = re.sub(pattern, f'({values_string})', updated_command, count=2)
            updated_command = re.sub(pattern, f'({cols_string})', updated_command, count=1)
            return updated_command


    def vacuum_helper(self,command):
        command_array = command.split()
        command_array[1] = random.choice(list(self.tables.keys()))
        return ' '.join(command_array)

    def delete_helper(self,command):
        command_array = command.split()
        random_table_name = random.choice(list(self.tables.keys()))
        command_array[2] = random_table_name
        if 'WHERE' in command:
            table_cols = self.tables[command_array[2]]
            if ' ' in table_cols[0]:
                col_name = table_cols[0][:table_cols[0].index(' ')]
            else:
                col_name = table_cols[0]
            command_array[4] = col_name
        return ' '.join(command_array)

    def pragma_helper(self,command):
        if 'table_xinfo' in command or 'table_info' in command or 'table_list' in command or 'quick_check' in command or 'foreign_key_check' in command or 'index_list' in command or 'integrity_check' in command:
            random_table_name = random.choice(list(self.tables.keys()))
            pattern = re.compile(r'\((.*?)\)')
            command = re.sub(pattern, f'({random_table_name})', command, count=1)
        elif 'index_xinfo' in command or 'index_xinfo' in command:
            random_index_name = random.choice(self.indexs)
            pattern = re.compile(r'\((.*?)\)')
            command = re.sub(pattern, f'({random_index_name})', command, count=1)
        return command

    def update_helper(self,command):
        command_array = command.split()
        random_table_name = random.choice(list(self.tables.keys()))
        command_array[1] = random_table_name
        table_cols = self.tables[command_array[1]]
        command = ' '.join(command_array)
        str1, str2 = command.split('SET', 1)
        str1 += 'SET'
        values = []
        for i in table_cols:
            if 'NUM' in i:
                if ' ' in i:
                    values.append(i[:i.index(' ')] + "=" + values.append(random.uniform(1.0, 100.0)))
                else:
                    values.append(i + "=" + values.append(random.uniform(1.0, 100.0)))
            elif 'INT' in i:
                if ' ' in i:
                    values.append(i[:i.index(' ')] + "=" + random.randint(1, 1000))
                else:
                    values.append(i + "=" + random.randint(1, 1000))
            elif 'TEXT' in i:
                x = generate_random_string(6)
                if ' ' in i:
                    values.append(i[:i.index(' ')] + "=" + "'" + x + "'")
                else:
                    values.append(i + "=" + "'" + x + "'")
            else:
                x = generate_random_string(6)
                if ' ' in i:
                    values.append(i[:i.index(' ')] + "=" + "'" + x + "'")
                else:
                    values.append(i + "=" + "'" + x + "'")
        values_string = ','.join(values)
        updated_command = str1 + ' ' + values_string + ';'
        return updated_command

    def alter_helper(self,command):
        command_array = command.split()
        random_table_name = random.choice(list(self.tables.keys()))
        command_array[2] = random_table_name
        table_cols = self.tables[command_array[2]]
        if 'RENAME TO' in command:
            new_name = generate_random_string(5)
            self.tables[new_name] = self.tables.pop(command_array[2])
            command_array[5] = new_name
        elif 'RENAME' in command:
            rand_col = random.choice(table_cols)
            replace_index = table_cols.index(rand_col)
            if ' ' not in rand_col:
                command_array[4] = rand_col
            else:
                command_array[4] = rand_col[: rand_col.index(' ')]
            command_array[6] = generate_random_string(5)
            self.tables[command_array[2]][replace_index] = command_array[6]
        elif 'ADD COLUMN' in command:
            col_desc = command_array[5] + command_array[6]
            self.tables[command_array[2]].append(col_desc)
        elif 'DROP COLUMN' in command:
            command_array[5] = random.choice(table_cols)
            self.tables[command_array[2]].remove(command_array[5])
            for each in self.tables:
                if self.tables[each] == []:
                    del self.tables[each]
        return ' '.join(command_array)


    def analyze_helper(self,command):
        command_array = command.split()
        rand_choice = random.choice(list(self.tables.keys()) + self.indexs)
        command_array[1] = rand_choice
        return ' '.join(command_array)

    def attach_helper(self, command):
        command_array = command.split()
        self.attached_db[command_array[2]] = command_array[4]
        return ' '.join(command_array)

    def detach_helper(self, command):
        command_array = command.split()
        rand_choice = random.choice(list(self.attached_db.keys()))
        command_array[2] = rand_choice
        del self.attached_db[command_array[2]]
        return ' '.join(command_array)

    def select_helper(self,command):
        if 'FROM' not in command:
            return command
        command_array = command.split()
        random_table_name = random.choice(list(self.tables.keys()))
        command_array[3] = random_table_name
        if '*' in command:
            return ' '.join(command_array)
        table_cols = self.tables[command_array[3]]
        if 'ORDER BY' in command or 'GROUP BY' in command:
            rand_choice = random.choice(table_cols)
            if ' ' in rand_choice:
                rand_choice = rand_choice[: rand_choice.index(' ')]
            command_array[-2] = rand_choice
        updated_command = ' '.join(command_array)
        updated_command_array = updated_command.split()
        if ',' not in updated_command_array[1]:
            rand_col = random.choice(table_cols)
            if ' ' in rand_col:
                rand_col = rand_col[: rand_col.index(' ')]
            updated_command_array[1] = rand_col
        else:
            rand_col1 = random.choice(table_cols)
            if ' ' in rand_col1:
                rand_col1 = rand_col1[: rand_col1.index(' ')]
            rand_col2 = random.choice(table_cols)
            if ' ' in rand_col2:
                rand_col2 = rand_col2[: rand_col2.index(' ')]
            updated_command_array[1] = rand_col1 + ',' + rand_col2
        return ' '.join(updated_command_array)

    def parse_command(self, command):
        if self.tables != {}:
            for i in self.tables:
                if i == []:
                    del self.tables[i]

        #Create Commands
        if command.startswith('CREATE'):
            return self.create_helper(command)

        #Drop Commands
        if command.startswith('DROP'):
            return self.drop_helper(command)

        #Insert/Replace Command
        elif command.startswith('INSERT') or command.startswith('REPLACE'):
            return self.insert_replace_helper(command)

        #Vacuum Command
        elif command.startswith('VACUUM'):
            return self.vacuum_helper(command)

        #Delete Command
        elif command.startswith('DELETE'):
            return self.delete_helper(command)

        #Pragma Command
        elif command.startswith('PRAGMA'):
            return self.pragma_helper(command)

        #Update Command
        elif command.startswith('UPDATE'):
            return self.update_helper(command)

        #Alter Command
        elif command.startswith('ALTER'):
            return self.alter_helper(command)

        #Analyze Command
        elif command.startswith('ANALYZE'):
            return self.analyze_helper(command)

        #Attach DB Command
        elif command.startswith('ATTACH'):
            return self.attach_helper(command)

        #Detach DB Command
        elif command.startswith('DETACH') and self.attached_db != {}:
            return self.detach_helper(command)

        #Select Command
        elif command.startswith('SELECT'):
            return self.select_helper(command)

        #SAVEPOINT Command
        elif command.startswith('SAVEPOINT'):
            command_array = command.split()
            self.savepoints.append(command_array[-1])
            return command

        #Release Command
        elif command.startswith('RELEASE'):
            command_array = command.split()
            random_name = random.choice(self.savepoints)
            command_array[-1] = random_name
            return ' '.join(command_array)

        #Rollback Command
        elif command.startswith('ROLLBACK'):
            command_array = command.split()
            random_name = random.choice(self.savepoints)
            command_array[-1] = random_name
            return ' '.join(command_array)

        #Explain Command
        elif command.startswith('EXPLAIN'):
            if 'SELECT' in command:
                s1, s2 = command.split('SELECT', 1)
                s2 = 'SELECT' + s2
                updated_nested_stmt = self.select_helper(s2)
                return s1 + updated_nested_stmt
            elif 'INSERT' in command:
                s1, s2 = command.split('INSERT', 1)
                s2 = 'INSERT' + s2
                updated_nested_stmt = self.insert_replace_helper(s2)
                return s1 + updated_nested_stmt
            elif 'REPLACE' in command:
                s1, s2 = command.split('REPLACE', 1)
                s2 = 'REPLACE' + s2
                updated_nested_stmt = self.insert_replace_helper(s2)
                return s1 + updated_nested_stmt
            elif 'UPDATE' in command:
                s1, s2 = command.split('UPDATE', 1)
                s2 = 'UPDATE' + s2
                updated_nested_stmt = self.update_helper(s2)
                return s1 + updated_nested_stmt
            elif 'VACUUM' in command:
                s1, s2 = command.split('VACUUM', 1)
                s2 = 'VACUUM' + s2
                updated_nested_stmt = self.vacuum_helper(s2)
                return s1 + updated_nested_stmt
            elif 'DELETE' in command:
                s1, s2 = command.split('DELETE', 1)
                s2 = 'DELETE' + s2
                updated_nested_stmt = self.delete_helper(s2)
                return s1 + updated_nested_stmt
            elif 'ALTER' in command:
                s1, s2 = command.split('ALTER', 1)
                s2 = 'ALTER' + s2
                updated_nested_stmt = self.alter_helper(s2)
                return s1 + updated_nested_stmt

        #Others - ON CONFLICT
        else:
            return command