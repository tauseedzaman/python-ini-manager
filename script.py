import configparser
import os

class IniFileManager:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.read_config()

    def read_config(self):
        """Reads the configuration from the file if it exists, otherwise creates an empty file."""
        if os.path.exists(self.config_file):
            self.config.read(self.config_file)
        else:
            open(self.config_file, 'w').close()

    def get_all_items(self):
        """Retrieves all items in the configuration file as a list of tuples."""
        config_list = [(section, key, value) for section in self.config.sections() for key, value in self.config.items(section)]
        default_items = self.config.defaults().items()
        config_list.extend([('DEFAULT', key, value) for key, value in default_items])
        return config_list

    def update_value(self, section, key, value):
        """Updates or adds a value in the specified section and key."""
        if not self.config.has_section(section) and section != 'DEFAULT':
            self.config.add_section(section)
        self.config[section][key] = value

    def delete_key(self, section, key):
        """Deletes a specific key from the specified section."""
        if self.config.has_section(section):
            self.config.remove_option(section, key)

    def delete_section(self, section):
        """Deletes an entire section."""
        if self.config.has_section(section):
            self.config.remove_section(section)

    def save_config(self):
        """Saves the current state of the configuration to the file."""
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

def main():
    while True:
        config_file = input("Enter the path to the .ini file: ")

        if not os.path.exists(config_file):
            print("\nFile does not exist.")
            print("1. Re-enter a valid path")
            print("2. Create a new .ini file at the specified path")
            choice = input("Enter your choice (1-2): ")
            
            if choice == '1':
                continue
            elif choice == '2':
                open(config_file, 'w').close()
                print(f"New .ini file created at {config_file}.")
            else:
                print("Invalid choice. Please enter 1 or 2.")
                continue

        manager = IniFileManager(config_file)

        while True:
            print("\nOptions:")
            print("1. View all items in the config file")
            print("2. Update a value")
            print("3. Add a new section and key")
            print("4. Delete a key")
            print("5. Delete a section")
            print("6. Save and exit")
            print("7. Exit without saving")

            choice = input("Enter your choice (1-7): ")

            if choice == '1':
                # View all items in the configuration file
                items = manager.get_all_items()
                if items:
                    print("\nAll items in the config file:")
                    for item in items:
                        print(item)
                else:
                    print("\nThe config file is empty or does not exist.")

            elif choice == '2':
                # Update a value in the configuration file
                section = input("Enter the section: ")
                key = input("Enter the key: ")
                value = input("Enter the new value: ")
                manager.update_value(section, key, value)

            elif choice == '3':
                # Add a new section and key in the configuration file
                section = input("Enter the section: ")
                key = input("Enter the key: ")
                value = input("Enter the value: ")
                manager.update_value(section, key, value)

            elif choice == '4':
                # Delete a specific key from a section
                section = input("Enter the section: ")
                key = input("Enter the key: ")
                manager.delete_key(section, key)

            elif choice == '5':
                # Delete an entire section
                section = input("Enter the section: ")
                manager.delete_section(section)

            elif choice == '6':
                # Save changes and exit
                manager.save_config()
                print("Configuration saved. Exiting...")
                return

            elif choice == '7':
                # Exit without saving changes
                print("Exiting without saving...")
                return

            else:
                print("Invalid choice. Please enter a number between 1 and 7.")

if __name__ == "__main__":
    main()
