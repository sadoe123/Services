import os

TEMPLATE_CONTENT = """\
<bean id="genericLovQueryService"
      class="com.linedata.chorus.std.services.commons.service.lov.service.impl.GenericLovQueryServiceImpl">
  <property name="frameworkJdbcTemplate" ref="chorusDaoTemplate" />
  <property name="sqlListOfValuesQuery">
    <map merge="true">
      {% for field in fields if field.isWithParam %}
      <entry key="{{ field.lov }}">
        <bean class="org.apache.commons.io.IOUtils" factory-method="toString">
          <constructor-arg type="java.io.InputStream"
            value="classpath:com/linedata/chorus/std/services/commons/dao/lovvalue/{{ field.sqlFile }}" />
        </bean>
      </entry>
      {% endfor %}
    </map>
  </property>
</bean>

{% for field in fields if not field.isWithParam %}
<bean id="{{ field.lov }}"
      class="com.linedata.chorus.std.services.commons.service.lov.service.impl.{{ field.lov }}">
  <property name="frameworkJdbcTemplate" ref="chorusDaoTemplate" />
  <property name="sqlListOfValuesQuery">
    <map merge="true">
      <entry key="{{ field.lov }}">
        <bean class="org.apache.commons.io.IOUtils" factory-method="toString">
          <constructor-arg type="java.io.InputStream"
            value="classpath:com/linedata/chorus/std/services/commons/dao/lovvalue/{{ field.sqlFile }}" />
        </bean>
      </entry>
    </map>
  </property>
</bean>
{% endfor %}
"""

def generate_jinja2_template(output_dir="output_templates", filename="lov_service_impl.spring.xml.j2"):
    """
    Génère un template Jinja2 corrigé pour les LOV services.
    """
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(TEMPLATE_CONTENT)
    
    print(f"✅ Template Jinja2 généré : {output_path}")

if __name__ == "__main__":
    generate_jinja2_template()

input("Appuyez sur Entrée pour fermer la console...")
