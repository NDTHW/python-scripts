from exchangelib import Credentials, Account, Configuration, DELEGATE, Folder
from exchangelib.protocol import BaseProtocol
from exchangelib import Message, Mailbox, HTMLBody
import os
from datetime import datetime

# Uncomment this line if your organization uses self-signed certificates
# BaseProtocol.VERIFY_SSL = False

class EnterpriseOutlookAutomation:
    def __init__(self, email, username=None, password=None):
        """
        Initialize connection to Exchange server using EWS
        
        Args:
            email: Your email address
            username: Your domain username (if different from email)
            password: Your password (can be None if using integrated authentication)
        """
        # Use domain authentication (common in enterprises)
        # If username is not provided, extract from email
        if not username:
            username = email.split('@')[0]
            
        credentials = Credentials(username, password)
        
        # Auto-discover Exchange server settings
        self.account = Account(
            primary_smtp_address=email,
            credentials=credentials,
            autodiscover=True,
            access_type=DELEGATE
        )
        
        # Get the inbox folder
        self.inbox = self.account.inbox
        
    def create_client_folder_structure(self, client_name):
        """
        Create a folder structure for a new client
        
        Args:
            client_name (str): Name of the client
            
        Returns:
            dict: Dictionary containing references to created folders
        """
        try:
            # Create main client folder under inbox
            main_folder = Folder(
                parent=self.inbox,
                name=client_name
            )
            main_folder.save()
            
            # Create subfolders
            subfolders = {}
            subfolder_names = [
                'Correspondence', 
                'Documents', 
                'Invoices', 
                'Contracts'
            ]
            
            for name in subfolder_names:
                subfolder = Folder(
                    parent=main_folder,
                    name=name
                )
                subfolder.save()
                subfolders[name] = subfolder
            
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
            Message: Created email message
        """
        try:
            # Read template
            with open(template_path, 'r') as file:
                template_content = file.read()

            # Replace placeholders
            if replacements:
                for key, value in replacements.items():
                    template_content = template_content.replace(f"[{key}]", str(value))

            # Create draft email in the drafts folder
            message = Message(
                account=self.account,
                folder=self.account.drafts,
                subject="",  # Will be set later
                body=HTMLBody(template_content)
            )
            
            return message
        
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
                
                message = self.create_email_from_template(template_path, replacements)
                if message:
                    message.subject = f"Welcome {client_name} - Partnership Information"
                    message.to_recipients = [Mailbox(email_address=client_email)]
                    
                    # Save to drafts (for review before sending)
                    message.save()
                    
                    print(f"Created welcome email draft for {client_name}")
            
            print(f"Completed new client setup for {client_name}")
            
        except Exception as e:
            print(f"Error in client setup: {e}")
    
    def create_inbox_rule(self, client_name, client_email, target_folder):
        """
        Note: Creating inbox rules with EWS is complex and often requires 
        specific permissions. This is a placeholder method.
        
        In enterprise environments, it's often better to:
        1. Create rules manually
        2. Have IT set up server-side rules
        3. Use Microsoft Flow/Power Automate for advanced rules
        """
        print(f"Creating inbox rules via EWS requires elevated permissions.")
        print(f"Please create a rule manually for {client_email} to move to {client_name} folder")

# Example usage with enterprise authentication
if __name__ == "__main__":
    # Replace with your information
    outlook = EnterpriseOutlookAutomation(
        email="your.name@company.com",
        # password is often not needed with domain authentication
        # password="your_password"  
    )
    
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