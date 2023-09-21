class Control_escalofon():
    @classmethod
    def obtener_empleado(self, db):
        try:
            cursor= db.connection.cursor()
            sql = """SELECT codigo, em.nombre, dni, c.nombre, id_cat, id_tipo, hrs_sem, hrs_men, fa.nombre FROM empleado AS em LEFT JOIN clase AS c ON em.id_clase = c.id_clase LEFT JOIN facultades AS fa ON em.id_facultad = fa.id_facultad"""
            cursor.execute(sql)
            row = cursor.fetchall()
            #row = cursor.fetchone()
            cursor.close()
            #db.connection.close()
            return row

        except Exception as ex:
            raise Exception(ex)
        
    def buscar_esc(self, db, query):
        try:
                cursor = db.connection.cursor()
                sql = """SELECT codigo, em.nombre, dni, c.nombre, id_cat, id_tipo, hrs_sem, hrs_men, fa.nombre FROM empleado AS em LEFT JOIN clase AS c ON em.id_clase = c.id_clase LEFT JOIN facultades AS fa ON em.id_facultad = fa.id_facultad WHERE em.nombre LIKE %s"""
                cursor.execute(sql, ("%" + query + "%",))
                rows = cursor.fetchall()
                cursor.close()
                return rows
        except Exception as ex:
            raise Exception(ex)
    
    def combobox_esc(self,db):
         try:
              cursor = db.connection.cursor()
              sql = "SELECT nombre FROM facultades"
              cursor.execute(sql)
              facultades = cursor.fetchall()
              cursor.close()
              return facultades
         except Exception as ex:
              raise Exception(ex)