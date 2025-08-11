${FunctionId}IRAPListBlockService.java
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