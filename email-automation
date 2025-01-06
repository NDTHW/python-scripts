import win32com.client
import os
from datetime import datetime

class OutlookAutomation:
    def __init__(self):
        """Initialize Outlook application object"""
        self.outlook = win32com.client.Dispatch('Outlook.Application')
        self.namespace = self.outlook.GetNamespace('MAPI')
        self.inbox = self.namespace.GetDefaultFolder(6)  # 6 represents the inbox folder

    def create_client_folder_structure(self, client_name):
        """
        Create a folder structure for a new client
        Args:
            client_name (str): Name of the client
        Returns:
            dict: Dictionary containing references to created folders
        """
        try:
            # Create main client folder
            main_folder = self.inbox.Folders.Add(client_name)
            
            # Create subfolders
            subfolders = {
                'Correspondence': main_folder.Folders.Add('Correspondence'),
                'Documents': main_folder.Folders.Add('Documents'),
                'Invoices': main_folder.Folders.Add('Invoices'),
                'Contracts': main_folder.Folders.Add('Contracts')
            }
            
            print(f"Created folder structure for {client_name}")
            return {'main': main_folder, **subfolders}
        
        except Exception as e:
            print(f"Error creating folder structure: {e}")
            return None

    def create_email_from_template(self, template_path, replacements=None):
        """
        Create an email from a template file
        Args:
            template_path (str): Path to the template file
            replacements (dict): Dictionary of placeholder replacements
        Returns:
            MailItem: Created email item
        """
        try:
            # Read template
            with open(template_path, 'r') as file:
                template_content = file.read()

            # Replace placeholders
            if replacements:
                for key, value in replacements.items():
                    template_content = template_content.replace(f"[{key}]", value)

            # Create email
            mail = self.outlook.CreateItem(0)  # 0 represents email item
            mail.HTMLBody = template_content
            
            return mail
        
        except Exception as e:
            print(f"Error creating email from template: {e}")
            return None

    def setup_new_client(self, client_name, client_email, template_path=None):
        """
        Setup everything needed for a new client
        Args:
            client_name (str): Name of the client
            client_email (str): Client's email address
            template_path (str): Path to welcome email template
        """
        try:
            # Create folder structure
            folders = self.create_client_folder_structure(client_name)
            
            if template_path and os.path.exists(template_path):
                # Create welcome email from template
                replacements = {
                    'CLIENT_NAME': client_name,
                    'DATE': datetime.now().strftime('%B %d, %Y')
                }
                
                mail = self.create_email_from_template(template_path, replacements)
                if mail:
                    mail.To = client_email
                    mail.Subject = f"Welcome {client_name} - Partnership Information"
                    # Display email for review before sending
                    mail.Display()
            
            print(f"Completed new client setup for {client_name}")
            
        except Exception as e:
            print(f"Error in client setup: {e}")

    def create_rule_for_client(self, client_name, client_email):
        """
        Create a rule to move emails from client to their folder
        Args:
            client_name (str): Name of the client
            client_email (str): Client's email address
        """
        try:
            # Note: Rules automation is more complex and might require
            # additional permissions or manual setup in some cases
            print(f"Please create a rule manually for {client_email} to move to {client_name} folder")
            
        except Exception as e:
            print(f"Error creating rule: {e}")

# Example usage
if __name__ == "__main__":
    # Initialize automation
    outlook = OutlookAutomation()
    
    # Setup new client
    client_info = {
        'name': 'Acme Corp',
        'email': 'contact@acmecorp.com',
        'template_path': 'templates/welcome_email.html'
    }
    
    outlook.setup_new_client(
        client_info['name'],
        client_info['email'],
        client_info['template_path']
    )