import os
from jinja2 import Environment, FileSystemLoader

TEMPLATE_DIR = "templates"
OUTPUT_DIR = "output"
OUTPUT_TEMPLATE_DIR = "output_templates"
FUNCTION_NAME = "MyFunction"  # <-- Change ici si besoin

# Créer les dossiers si besoin
os.makedirs(TEMPLATE_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_TEMPLATE_DIR, exist_ok=True)

# --- Template FormService (GENERIC) ---
formservice_template_content = """${FunctionId}IRAPFormService.java
package com.linedata.chorus.std.gui;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import com.linedata.chorus.std.services.utils.UtilsService;
import com.linedata.ekip.commons.shared.context.ActionContext;
import com.linedata.ekip.commons.shared.lov.LovOpenFunctionMode;
import com.linedata.ekip.core.server.screenservices.FormService;
import com.linedata.ekip.core.shared.context.functionalcontext.FunctionalContext;
import com.linedata.ekip.core.shared.context.screencontext.ScreenContext;
import com.linedata.ekip.core.shared.data.Data;
import com.linedata.ekip.core.shared.lov.LovEvent;

@Component
public class ${FunctionId}IRAPFormService implements FormService
{
    public static final String BEANID = "${FunctionId}IRAPFormService";

    @Autowired
    UtilsService utilsService;

    @Override
    public String getBeanId()
    {
        return BEANID;
    }

    @Override
    public Data provideData(ActionContext actionContext, LovEvent event,
                            LovOpenFunctionMode openFunctionMode, ScreenContext screenContext, Data inParameters,
                            FunctionalContext functionalContext)
    {
        if (event.getValue().equals(LovEvent.SCREENOPENED.getValue()) &&
            inParameters.get("SCREENID").equals("${FunctionId}IRAP"))
        {
            Data data = new Data();
            String xidlog = utilsService.xlogCreate("${FunctionId.toUpperCase()}C");
            String xidclg = utilsService.getXetbXidclg();
            String xidcev = utilsService.getXetbXidcev();
            data.set("xidlog", xidlog);
            data.set("xidclg", xidclg);
            data.set("reiv_xidcev", xidcev);
            return data;
        }
        return null;
    }
}
"""

# --- Template GridService (GENERIC) ---
gridservice_template_content = """${FunctionId}IRAPListBlockService.java
package com.linedata.chorus.std.gui;

import java.util.ArrayList;
import java.util.List;
import javax.annotation.Resource;
import org.dozer.DozerBeanMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import com.linedata.chorus.std.services.utils.UtilsService;
import com.linedata.ekip.commons.shared.context.ActionContext;
import com.linedata.ekip.commons.shared.lov.LovOpenFunctionMode;
import com.linedata.ekip.core.server.screenservices.GridService;
import com.linedata.ekip.core.shared.context.functionalcontext.FunctionalContext;
import com.linedata.ekip.core.shared.context.screencontext.ScreenContext;
import com.linedata.ekip.core.shared.data.Data;
import com.linedata.ekip.core.shared.lov.LovEvent;

@Component
public class ${FunctionId}IRAPListBlockService implements GridService
{
    private static final String BEANID = "${FunctionId}IRAPListBlockService";

    @Autowired
    private ${FunctionId}Service ${functionId}Service;

    @Resource(name = "ReportMapper")
    protected DozerBeanMapper mapper;

    @Autowired
    private UtilsService utilsService;

    public String getBeanId()
    {
        return BEANID;
    }

    @Override
    public List<Data> provideData(ActionContext actionContext, LovEvent event,
                                  LovOpenFunctionMode openFunctionMode, ScreenContext screenContext, Data inParameters,
                                  FunctionalContext functionalContext)
    {
        List<Data> result = new ArrayList<>();
        Data formData = inParameters.get("DATASERVICEPARAMETER");

        if (formData != null && formData.get("xidlog") != null)
            utilsService.xlogUpdate(formData.get("xidlog"), "${FunctionId}I");

        // Dummy mapping
        // List<${FunctionId}> list = ${functionId}Service.getData();
        // for (${FunctionId} item : list) {
        //     Data data = mapper.map(item, Data.class);
        //     result.add(data);
        // }

        return result;
    }
}
"""

# --- Template FunctionService (GENERIC) ---
functionservice_template_content = """${FunctionId}FunctionService.java
package com.linedata.chorus.std.gui.${functionId};
import java.util.Collection;
import java.util.Map;
import java.util.List;
import java.util.ArrayList;
import javax.annotation.Resource;
import org.dozer.DozerBeanMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import com.linedata.chorus.std.entity.${functionId}IRAP.${functionId}IRAP;
import com.linedata.chorus.std.entity.${functionId}IRAP.impl.${functionId}IRAPImpl;
import com.linedata.chorus.std.gui.commons.server.ExceptionManager;
import com.linedata.chorus.std.services.Report.impl.BIPRWSService;
import com.linedata.chorus.std.services.Report.impl.BOExportService;
import com.linedata.chorus.std.services.Report.impl.BOLoginService;
import com.linedata.chorus.std.services.Report.impl.ReportRefresher;
import com.linedata.chorus.std.services.Report.impl.ScriptExecutorService;
import com.linedata.chorus.std.services.irap.GenericReportService;
import com.linedata.chorus.std.services.commons.jdbc.ChorusStoredProcedure;
import com.linedata.chorus.std.services.commons.service.exception.ChorusServiceException;
import com.linedata.ekip.commons.shared.context.ActionContext;
import com.linedata.ekip.commons.shared.lov.LovContextType;
import com.linedata.ekip.commons.shared.lov.LovOpenFunctionMode;
import com.linedata.ekip.commons.shared.lov.LovRedirectTargetType;
import com.linedata.ekip.core.server.screenservices.ScreenService;
import com.linedata.ekip.core.shared.asi.screenaction.postaction.AsiOpenFunction;
import com.linedata.ekip.core.shared.context.screencontext.ScreenContext;
import com.linedata.ekip.core.shared.data.Data;
import com.linedata.ekip.core.shared.data.ScreenServiceResponse;
import com.linedata.ekip.core.shared.lov.LovScreenServiceReturnCode;
@Component
public class ${FunctionId}IRAPFunctionService extends ScreenService
{
 private static final String BEANID = "${FunctionId}IRAPFunctionService";
 @Autowired
 protected ChorusStoredProcedure chorusStoredProcedure;
 @Autowired
 private GenericReportService genericService;
 public static final Integer ICDDEP_NO = Integer.valueOf(0);
 public static final int DEFAULT_IIDLAN = 1;
 @Resource(name = "ReportMapper")
 protected DozerBeanMapper mapper;
 @Resource(name = "ExceptionManager")
 private ExceptionManager exceptionManager;
 public static String baseUrl = "http://172.25.32.113:8080";
 @Override
 public String getBeanId()
 {
 return BEANID;
 }
 @Override
 public void manageActionMappings()
 {
 getActionMappings().put("launch", "launch");
 }
 public static List<Map<String, Object>> filterSelectedData(List<Map<String, Object>> dataList) {
 List<Map<String, Object>> result = new ArrayList<>();
 for (Map<String, Object> data : dataList) {
 Object value = data.get("select_report");
 if (Boolean.TRUE.equals(value) || (value instanceof Integer && ((Integer) value) == 1)) {
 result.add(data);
 }
 }
 return result;
}
 public ScreenServiceResponse launch(ActionContext actionContext, String functionId,
ScreenContext screenContext, Data inParameters) throws Exception
 {
 String username = genericService.getUserName();
 String password = genericService.getPassword();
 int iidlan;
 String documentId = "";
 String documentCUID = "";
 String extension = "";
 String exportPath = "C:\\dev\\tools\\apache-tomcat-Chorus\\webapps\\REPORT\\";
 ScreenServiceResponse screenServiceResponse = initScreenServiceResponse(screenContext);
 screenContext.getOthersParameters();
 Data ${FunctionId}ReportGeneric = inParameters.get(${functionId}+"BlockForm");
 List<Data> reportList = inParameters.get(${functionId}+"BlockList");
 List<Data> selectedReportList=filterSelectedData(reportList);
 ${FunctionId}IRAP ${functionId}irap = mapper.map(${FunctionId}ReportGeneric, ${FunctionId}IRAPImpl.class);
 try
 {
 String className = ${FunctionId}.getClass().toString();
 Collection<String> ${functionId}ReportGenericNames = ${functionId}ReportGeneric.getPropertyNames();
 Collection<Integer> fieldsReportNumber = genericService.generateLunchNumber(${FunctionId}ReportGenericNames, className);
 Map<String, Object> map = genericService.generateReport(${FunctionId}irap, fieldsReportNumber);
 iidlan = (Integer) map.get("iidlan0");
 ScriptExecutorService executor = new ScriptExecutorService();
 String response = executor.executeScript(iidlan);
 String promptValue = String.valueOf(iidlan);
 String reportIdentifier="";
 for( int i=0; i<selectedReportList.size();i++){
 extension=(String)selectedReportList.get(i).get("extension");
 documentCUID=(String)selectedReportList.get(i).get("documentCUID");
 String reportName = reportIdentifier + promptValue + extension;
 exportPath = exportPath.concat(reportName);
 String token = BOLoginService.login(username, password);
 ReportRefresher refresher = new ReportRefresher(token);
 BIPRWSService detailsReport = new BIPRWSService(baseUrl);
 try
 {
 documentId = detailsReport.getDocumentIdFromCuid(documentCUID, token);
 refresher.refreshDocument(documentId, promptValue);
 }
 catch (Exception e)
 {
 System.err.println("Erreur lors de la mise à jour du document :");
 e.printStackTrace();
 }
StringBuilder fileNameBuilder = new StringBuilder();
 switch (extension)
 {
 case ".pdf":
 BOExportService.exportPdf(token, documentId, exportPath);
 fileNameBuilder.append("/REPORT");
 break;
 case ".xlsx":
 BOExportService.exportExcel(token, documentId, exportPath);
 fileNameBuilder.append("/IRAP");
 break;
 case ".csv":
BOExportService.exportCSV(token, documentId, exportPath);
 fileNameBuilder.append("/IRAP");
 break;
 case ".txt":
 BOExportService.exportText(token, documentId, exportPath);
 fileNameBuilder.append("/IRAP"); 
 break;
 default:
 System.out.println("Extension inconnue.");
 break;
 }
 fileNameBuilder.append("/" + reportName);
 screenContext.getOthersParameters().set("path", fileNameBuilder.toString());
 AsiOpenFunction asiOpenFunction = new AsiOpenFunction();
 asiOpenFunction.setFunctionId("DocBrowse");
 asiOpenFunction.setOpenFunctionMode(LovOpenFunctionMode.CREATE);
 asiOpenFunction.setContext(LovContextType.SCREEN);
 asiOpenFunction.setSortNumber(1);
 asiOpenFunction.setTarget(LovRedirectTargetType.TAB);
 asiOpenFunction.setCloseActiveFunction(false);
 screenServiceResponse.getScreenPostActions().add(asiOpenFunction);
 screenServiceResponse.setReturnCode(LovScreenServiceReturnCode.CUSTOM);
 }
 }
 catch (ChorusServiceException e)
 {
 e.printStackTrace();
 screenServiceResponse.setReturnCode(LovScreenServiceReturnCode.ERROR);
 return screenServiceResponse;
 }
 return screenServiceResponse;
 }
}
"""

# --- Génération des trois templates dans output_templates avec les bons noms ---
templates = [
    ("${FunctionId}IRAPFormService.java.j2", formservice_template_content),
    ("${FunctionId}IRAPListBlockService.java.j2", gridservice_template_content),
    ("${FunctionId}FunctionService.java.j2", functionservice_template_content)
]

for filename, content in templates:
    output_path = os.path.join(OUTPUT_TEMPLATE_DIR, filename)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"📝 Template généré : {output_path}")
    