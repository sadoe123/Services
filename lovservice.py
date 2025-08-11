import os

TEMPLATE_CONTENT = """\

<property name="sqlListOfValuesQuery">
  <map merge="true">
    {% for field in fields if not field.isWithParam %}
    <entry key="${{{ field.fieldId }}}{{ functionId }}_valuesList_01">
      <bean class="org.apache.commons.io.IOUtils" factory-method="toString">
        <constructor-arg type="java.io.InputStream"
          value="classpath:com/linedata/chorus/std/services/commons/dao/lovvalue/{{ field.fieldId }}{{ functionId }}_valuesList_01.sql" />
      </bean>
    </entry>
    {% endfor %}
  </map>
</property>


{% for field in fields if field.isWithParam %}
<bean id="{{ field.fieldId }}{{ functionId }}LovQueryService"
      class="com.linedata.chorus.std.services.commons.service.lov.service.impl.{{ field.fieldId }}{{ functionId }}LovQueryServiceImpl">
  <property name="frameworkJdbcTemplate" ref="chorusDaoTemplate" />
  <property name="sqlListOfValuesQuery">
    <map merge="true">
      <entry key="{{ field.fieldId }}{{ functionId }}LovQueryService">
        <bean class="org.apache.commons.io.IOUtils" factory-method="toString">
          <constructor-arg type="java.io.InputStream"
            value="classpath:com/linedata/chorus/std/services/commons/dao/lovvalue/{{ field.fieldId }}{{ functionId }}_valuesList_01.sql" />
        </bean>
      </entry>
    </map>
  </property>
</bean>
{% endfor %}
"""

def generate_jinja2_template(output_dir="output_templates", filename="lov_service_impl.spring.xml.j2"):
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(TEMPLATE_CONTENT)
    print(f"✅ Template Jinja2 généré : {output_path}")


if __name__ == "__main__":
    generate_jinja2_template()
