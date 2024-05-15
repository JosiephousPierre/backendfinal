# model/consulted_medication.py
from fastapi import Depends, HTTPException, APIRouter, Form, status
from .db import get_db


ConsultedMedicationRouter = APIRouter(tags=["Consulted Medication"])

# CRUD operations

@ConsultedMedicationRouter.get("/consulted_medication/", response_model=list)
async def read_consulted_medications(
    db=Depends(get_db)
):
    query = "SELECT prescription_Id, Consultation_Id, medicine_ID, quantity FROM consulted_med"
    db[0].execute(query)
    consulted_medications = [{
            "prescription_Id": row[0],
            "Consultation_Id": row[1],
            "medicine_ID": row[2],
            "quantity": row[3]
        } 
            for row in db[0].fetchall()]
    return consulted_medications

@ConsultedMedicationRouter.get("/consulted_medication/{prescription_Id}", response_model=dict)
async def read_consulted_medication(
    prescription_Id: int, 
    db=Depends(get_db)
):
    query = "SELECT prescription_Id, Consultation_Id, medicine_ID, quantity FROM consulted_med WHERE prescription_Id = %s"
    db[0].execute(query, (prescription_Id,))
    consulted_medication = db[0].fetchone()
    if consulted_medication:
        return {
            "prescription_Id": consulted_medication[0],
            "Consultation_Id": consulted_medication[1],
            "medicine_ID": consulted_medication[2],
            "quantity": consulted_medication[3]
        }
    raise HTTPException(status_code=404, detail="Consulted Medication not found")

@ConsultedMedicationRouter.post("/consulted_medication/", response_model=dict)
async def create_consulted_medication(
    Consultation_Id: int = Form(...),
    medicine_ID: int = Form(...),
    quantity: int = Form(...),
    db=Depends(get_db)
):

    # Check if there is enough quantity in the manage_med table
    check_query = "SELECT quantity FROM manage_med WHERE medicine_ID = %s"
    db[0].execute(check_query, (medicine_ID,))
    manage_med_quantity = db[0].fetchone()

    if not manage_med_quantity or quantity > manage_med_quantity[0]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough quantity of medicine")

    # Update the quantity in the manage_med table
    update_query = "UPDATE manage_med SET quantity = quantity - %s WHERE medicine_ID = %s"
    db[0].execute(update_query, (quantity, medicine_ID))

    # Insert the consulted medication
    insert_query = "INSERT INTO consulted_med (Consultation_Id, medicine_ID, quantity) VALUES (%s, %s, %s)"
    db[0].execute(insert_query, (Consultation_Id, medicine_ID, quantity))

    # Retrieve the last inserted ID using LAST_INSERT_ID()
    db[0].execute("SELECT LAST_INSERT_ID()")
    new_prescription_Id = db[0].fetchone()[0]
    db[1].commit()

    return {
        "prescription_Id": new_prescription_Id,
        "Consultation_Id": Consultation_Id,
        "medicine_ID": medicine_ID,
        "quantity": quantity
    }


@ConsultedMedicationRouter.put("/consulted_medication/{prescription_Id}", response_model=dict)
async def update_consulted_medication(
    prescription_Id: int,
    Consultation_Id: int = Form(...),
    medicine_ID: int = Form(...),
    quantity: int = Form(...),
    db=Depends(get_db)
):
    try:
        # Get the current medicine_ID and quantity of the consulted medication
        query_get_medicine_info = "SELECT medicine_ID, quantity FROM consulted_med WHERE prescription_Id = %s"
        db[0].execute(query_get_medicine_info, (prescription_Id,))
        current_medicine_info = db[0].fetchone()

        if not current_medicine_info:
            raise HTTPException(status_code=404, detail="Consulted Medication not found")

        current_medicine_ID, current_quantity = current_medicine_info

        # Calculate the quantity difference for the current and new medicine IDs
        quantity_difference = quantity - current_quantity

        # Scenario 1: Changing consult_med quantity only
        if current_medicine_ID == medicine_ID:
            query_update_manage_med = "UPDATE manage_med SET quantity = quantity - %s WHERE medicine_ID = %s"
            db[0].execute(query_update_manage_med, (quantity_difference, medicine_ID))

        # Scenario 2: Changing consult_med medicine_ID only
        elif current_quantity == quantity:
            query_update_manage_med_current = "UPDATE manage_med SET quantity = quantity + %s WHERE medicine_ID = %s"
            db[0].execute(query_update_manage_med_current, (current_quantity, current_medicine_ID))
            query_update_manage_med_new = "UPDATE manage_med SET quantity = quantity - %s WHERE medicine_ID = %s"
            db[0].execute(query_update_manage_med_new, (current_quantity, medicine_ID))

        # Scenario 3: Changing both consult_med quantity and medicine_ID
        else:
            # Revert previous stock changes for the current medicine_ID
            query_update_manage_med_current = "UPDATE manage_med SET quantity = quantity + %s WHERE medicine_ID = %s"
            db[0].execute(query_update_manage_med_current, (current_quantity, current_medicine_ID))

            # Apply stock changes for the new medicine_ID
            query_update_manage_med_new = "UPDATE manage_med SET quantity = quantity - %s WHERE medicine_ID = %s"
            db[0].execute(query_update_manage_med_new, (quantity, medicine_ID))

        # Update the consulted medication information in the database
        query_update_consulted_med = "UPDATE consulted_med SET Consultation_Id = %s, medicine_ID = %s, quantity = %s WHERE prescription_Id = %s"
        db[0].execute(query_update_consulted_med, (Consultation_Id, medicine_ID, quantity, prescription_Id))

        # Commit the changes
        db[1].commit()

        return {"message": "Consulted Medication updated successfully"}

    except Exception as err:
        db[1].rollback()
        raise HTTPException(status_code=500, detail="Error updating consulted medication.") from err



@ConsultedMedicationRouter.delete("/consulted_medication/{prescription_Id}", response_model=dict)
async def delete_consulted_medication(
    prescription_Id: int,
    db=Depends(get_db)
):
    try:
        # Check if the consulted medication exists
        query_check_consulted_medication = "SELECT prescription_Id, medicine_ID, quantity FROM consulted_med WHERE prescription_Id = %s"
        db[0].execute(query_check_consulted_medication, (prescription_Id,))
        consulted_medication = db[0].fetchone()

        if not consulted_medication:
            raise HTTPException(status_code=404, detail="Consulted Medication not found")

        # Delete the consulted medication
        query_delete_consulted_medication = "DELETE FROM consulted_med WHERE prescription_Id = %s"
        db[0].execute(query_delete_consulted_medication, (prescription_Id,))
        db[1].commit()

        # Add the quantity back to the manage_med table
        update_query = "UPDATE manage_med SET quantity = quantity + %s WHERE medicine_ID = %s"
        db[0].execute(update_query, (consulted_medication[2], consulted_medication[1]))
        db[1].commit()

        return {"message": "Consulted Medication deleted successfully"}
    except Exception as e:
        # Handle other exceptions if necessary
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the database cursor
        db[0].close()


