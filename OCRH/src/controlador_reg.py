from flask import current_app

class Control_reg():

    @classmethod
    def obtener_reg(self, db):
        try:
            cursor= db.connection.cursor()
            sql = """SELECT reg.id_reg, em.id_clase, em.dni, em.codigo, em.id_cat, em.id_tipo, em.hrs_sem, em.hrs_men, em.nombre, fa.nombre, reg.anexo_uno, reg.anexo_dos, reg.hrs_ci, reg.hrs_cni, reg.tot_hrs_dic, reg.hrs_des, reg.observaciones FROM registros AS reg LEFT JOIN empleado AS em ON reg.codigo = em.codigo LEFT JOIN facultades AS fa ON em.id_facultad = fa.id_facultad"""
            cursor.execute(sql)
            row = cursor.fetchall()
            #row = cursor.fetchone()
            cursor.close()
            #db.connection.close()
            return row

        except Exception as ex:
            raise Exception(ex)
    
    def insertar_reg(self,db,codper,iduser,aneuno,anedos,hrsci,hrscni, tothrs, hrsdes, observacion, anoreg, mesreg, diareg):
        try:
            cursor = db.connection.cursor()
            cursor.execute("INSERT INTO registros (codigo, id_user, anexo_uno, anexo_dos, hrs_ci, hrs_cni, tot_hrs_dic, hrs_des, observaciones, ano_reg, mes_reg, dia_reg) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (codper, iduser, aneuno, anedos, hrsci, hrscni, tothrs, hrsdes, observacion, anoreg, mesreg, diareg))
            db.connection.commit()
            cursor.close()
        except Exception as ex:
            raise Exception(ex)
    
    def buscar_reg(self, db, query):
        try:
                cursor = db.connection.cursor()
                sql = """SELECT reg.id_reg, em.id_clase, em.dni, em.codigo, em.id_cat, em.id_tipo, em.hrs_sem, em.hrs_men, em.nombre, fa.nombre, reg.anexo_uno, reg.anexo_dos, reg.hrs_ci, reg.hrs_cni, reg.tot_hrs_dic, reg.hrs_des, reg.observaciones FROM registros AS reg LEFT JOIN empleado AS em ON reg.codigo = em.codigo LEFT JOIN facultades AS fa ON em.id_facultad = fa.id_facultad WHERE em.nombre LIKE %s"""
                cursor.execute(sql, ("%" + query + "%",))
                rows = cursor.fetchall()
                cursor.close()
                return rows
        except Exception as ex:
            raise Exception(ex)