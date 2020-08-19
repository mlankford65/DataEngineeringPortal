from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, SelectField
from wtforms.validators import DataRequired
import yaml
import pyodbc

class ServerTableForm(FlaskForm):
    def Get_ConfigData():
        with open('config.yaml') as f:
            configData = yaml.load(f, Loader=yaml.FullLoader)

        return configData

    def Get_ServerDomains(configData, cursor):
        query =  "SELECT [Server_Domain_Desc] FROM [dbo].[Server_Domain] WHERE [Server_Domain_Desc] <> [Extension_Domain] ORDER BY [Server_Domain_Desc]"
        domains = []
        cursor.execute(query)
        
        if ( cursor is not None):
            for row in cursor:
                domains.append( row.Server_Domain_Desc )

        return domains

    def Get_ServerTypes(configData, cursor):
        query =  "SELECT [Server_Type_Desc] FROM [dbo].[Server_Type] ORDER BY [Server_Type_Desc]"
        serverTypes = []
        cursor.execute(query)
        
        if ( cursor is not None):
            for row in cursor:
                serverTypes.append( row.Server_Type_Desc )

        return serverTypes
 
    def Get_ServerClassifications(configData, cursor):
        query =  "SELECT [Server_Classification_Desc] FROM [dbo].[Server_Classification] ORDER BY [Server_Classification_Desc]"
        serverClassification = []
        cursor.execute(query)
        
        if ( cursor is not None):
            for row in cursor:
                serverClassification.append( row.Server_Classification_Desc )

        return serverClassification

    def Get_ServerTransitionTypes(configData, cursor):
        query =  "SELECT [Server_Transition_Desc] FROM [dbo].[Server_Type_Transition] ORDER BY [Server_Transition_Desc]"
        serverTransitionTypes = []
        cursor.execute(query)
        
        if ( cursor is not None):
            for row in cursor:
                serverTransitionTypes.append( row.Server_Transition_Desc )

        return serverTransitionTypes

    def Get_Services(configData, cursor):
        query =  """
            SELECT 
                   CASE 
                       WHEN [Service_Description] IS NULL
                           THEN [Service_Abbreviation]
                       ELSE
                            [Service_Abbreviation] + ' - ' + [Service_Description]
                    END AS [Service_Description]
              FROM 
                   [dbo].[Service] 
             WHERE 
                   Active = 1 
             ORDER BY 
                   [Service_Description]
        """
        services = []
        cursor.execute(query)
        
        if ( cursor is not None):
            for row in cursor:
                services.append( row.Service_Description )

        return services

    configData = Get_ConfigData()

    connectionString = 'DRIVER={SQL Server};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s;' % (configData["ConfigInstance"], configData["ConfigDatabase"], configData["ConfigUID"], configData["ConfigPWD"])
    conn = pyodbc.connect(connectionString)
    cursor = conn.cursor()

    serverDomains = Get_ServerDomains(configData, cursor)
    serverTypes = Get_ServerTypes(configData, cursor)
    serverClassifications = Get_ServerClassifications(configData, cursor)
    serverTransitionTypes = Get_ServerTransitionTypes(configData, cursor)
    services = Get_Services(configData, cursor)

    serverName = StringField( label='Server Name:', validators=[DataRequired()] )
    serverDomain = SelectField( label='Domain:', choices=serverDomains, default=1 )
    serverType = SelectField( label='Server Type:', choices=serverTypes, default=1 )
    serverClassification = SelectField( label='Classification:', choices=serverClassifications, default=1 )
    serverTransitionType = SelectField( label='Transition:', choices=serverTransitionTypes, default=1 )
    port = StringField( label='Port:', validators=[DataRequired()] )
    service = SelectField( label='Service:', choices=services, default=1 )
    vlan = StringField( label='VLAN:', validators=[DataRequired()] )
    maintenanceMode = RadioField( label='Maintenance Mode:', choices=[('yes', 'No'), ('yes', 'Yes')] )
    isActive = RadioField( label='Is Active:', choices=[('yes', 'No'), ('yes', 'Yes')] )
    crNumber = StringField( label='CR Number:', validators=[DataRequired()] )
    caseNumber = StringField( label='Case Number:', validators=[DataRequired()] )
    serverInfo = StringField( label='Server Information:', validators=[DataRequired()] )
    requiredFields = StringField( label='* Indicates Required Field' )

    clear = SubmitField('Clear Form') 
    submit = SubmitField('Submit') 
    cancel = SubmitField('Cancel') 
