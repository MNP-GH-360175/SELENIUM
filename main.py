
from lead_creation import create_lead
from lead_update_saleshead import update_lead_status
from customer_details_salesofficer import enter_customer_details
from sanction_branchmanager import sanction_lead

def run_full_workflow():
    # Step 1: Create lead (assume it returns lead_id)
    lead_id = create_lead()  # Modify create_lead to return ID if possible
    
    # Step 2: Sales Head update
    update_lead_status(lead_id)
    
    # Step 3: Sales Officer details
    enter_customer_details(lead_id)
    
    # Step 4: Branch Manager sanction
    sanction_lead(lead_id)
    
    print("Full workflow completed!")

if __name__ == "__main__":
    run_full_workflow()