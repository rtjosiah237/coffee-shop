class ScheduleManager:
    def __init__(self, db):
        self.db = db
    
    def view_barista_schedule(self):
        ssn = input("Barista SSN: ").strip()
        rows = self.db.run_query(
            """
            SELECT day_of_week, start_time, end_time
              FROM Barista_Schedule
             WHERE barista_ssn = :ssn
             ORDER BY day_of_week, start_time
            """,
            ssn=ssn
        )
        if not rows:
            print("No shifts found.")
            return
        
        print("\nDay       Start   End")
        print("----------------------")
        for day, st, et in rows:
            print(f"{day:<9}  {st}  {et}")
    
    def add_barista_shift(self):
        ssn   = input("Barista SSN: ").strip()
        day   = input("Day (Monday, Tuesday, etc.): ").strip()
        stime = input("Start (HH:MM:SS): ").strip()
        etime = input("End   (HH:MM:SS): ").strip()
        try:
            self.db.begin()
            self.db.run_query(
                """
                INSERT INTO Barista_Schedule
                  (barista_ssn, day_of_week, start_time, end_time)
                VALUES (:ssn, :day, :stime, :etime)
                """,
                ssn=ssn, day=day, stime=stime, etime=etime
            )
            self.db.commit()
            print("Shift added.")
        except Exception as e:
            self.db.rollback()
            print(f"Error adding shift: {e}")
    
    def edit_barista_shift(self):
        ssn    = input("Barista SSN: ").strip()
        day    = input("Day (Monday, Tuesday, etc.): ").strip()
        old_st = input("Current start (HH:MM:SS): ").strip()
        new_st = input("New start: ").strip()
        new_et = input("New end: ").strip()
        try:
            self.db.begin()
            self.db.run_query(
                """
                UPDATE Barista_Schedule
                   SET start_time = :new_st, end_time = :new_et
                 WHERE barista_ssn = :ssn
                   AND day_of_week = :day
                   AND start_time  = :old_st
                """,
                ssn=ssn, day=day, old_st=old_st, new_st=new_st, new_et=new_et
            )
            self.db.commit()
            print("Shift updated.")
        except Exception as e:
            self.db.rollback()
            print(f"Error updating shift: {e}")
    
    def delete_barista_shift(self):
        ssn = input("Barista SSN: ").strip()
        day = input("Day (Monday, Tuesday, etc.): ").strip()
        st  = input("Start time (HH:MM:SS): ").strip()
        try:
            self.db.begin()
            self.db.run_query(
                """
                DELETE FROM Barista_Schedule
                 WHERE barista_ssn = :ssn
                   AND day_of_week = :day
                   AND start_time  = :st
                """,
                ssn=ssn, day=day, st=st
            )
            self.db.commit()
            print("Shift deleted.")
        except Exception as e:
            self.db.rollback()
            print(f"Error deleting shift: {e}")