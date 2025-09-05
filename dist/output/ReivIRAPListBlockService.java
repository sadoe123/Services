package com.linedata.chorus.std.gui;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

import javax.annotation.Resource;

import org.dozer.DozerBeanMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import com.linedata.chorus.std.services.objectconverters.DateFormatter;
import com.linedata.chorus.std.services.utils.UtilsService;
import com.linedata.chorus.std.services.reports.GenericReportService;

import com.linedata.ekip.commons.server.log.LogFactory;
import com.linedata.ekip.commons.server.log.Logger;
import com.linedata.ekip.commons.shared.context.ActionContext;
import com.linedata.ekip.commons.shared.lov.LovOpenFunctionMode;
import com.linedata.ekip.core.server.screenservices.GridService;
import com.linedata.ekip.core.shared.context.functionalcontext.FunctionalContext;
import com.linedata.ekip.core.shared.context.screencontext.ScreenContext;
import com.linedata.ekip.core.shared.data.Data;
import com.linedata.ekip.core.shared.lov.LovEvent;

import com.linedata.chorus.std.entity.reivIRAP.reivIRAP;
import com.linedata.chorus.std.entity.reivIRAP.impl.reivIRAPImpl;

@Component
public class ReivIRAPListBlockService implements GridService
{
    private static final String BEANID = "ReivIRAPListBlockService";
    private final Logger logger = LogFactory.getLog(ReivIRAPListBlockService.class);

    @Autowired
    private ReivService reivService;

    @Resource(name = "ReportMapper")
    protected DozerBeanMapper mapper;

    @Autowired
    private UtilsService utilsService;

    @Autowired
    private GenericReportService genericService;

    public String getBeanId()
    {
        return BEANID;
    }

    @Override
    public List<? extends Data> provideData(ActionContext actionContext, LovEvent event,
                                            LovOpenFunctionMode openFunctionMode,
                                            ScreenContext screenContext,
                                            Data inParameters,
                                            FunctionalContext functionalContext)
    {
        List<Data> result = new ArrayList<>();
        Data formData = inParameters.get("DATASERVICEPARAMETER");

        if (formData != null && formData.get("xidlog") != null)
        {
            utilsService.xlogUpdate(formData.get("xidlog"), "ReivI");
        }

        reivIRAP reivirap = mapper.map(formData, reivIRAPImpl.class);
        String iidrap = genericService.getReportsId(reivirap);
        reivirap.setIidrap(iidrap);

        List<ReivIRAP> reivList = genericService.getGridList(reivirap);

        for (ReivIRAP item : reivList)
        {
            if (item != null)
            {
                Data data = mapper.map(item, Data.class);
                result.add(data);
            }
        }

        return result;
    }
}