"""Code samples for the preview, one per language, in pairs that share a row.

Markup: «key:text» highlights text with a text attribute key or an alias from heritage.preview.ALIASES.
Unmarked words use TEXT and unmarked punctuation uses DEFAULT_OPERATION_SIGN. Each sample is
(file name, line with the caret or None, code).

Samples use a language's own keys where its plugin is bundled with IntelliJ IDEA, PyCharm or WebStorm.
Go, C, C++ and C# use the DEFAULT_* keys their highlighting falls back to.
"""

JAVA = ("OrderController.java", 9, """\
«doc:/** Handles orders. »«dt:@since»«doc: 1.0 */»
«an:@Controller»(«st:"/orders"»)
«kw:public class» «ty:OrderController» {
    «kw:private static final int» «co:MAX_ITEMS» = «nu:42»;
    «kw:private final» «ty:OrderService» «fd:service»;

    «an:@Get»(«st:"/{id}"»)
    «kw:public» «ty:Optional»<«ty:Order»> «fn:find»(«ty:Long» «pa:id») {
        «kw:return» «fd:service».«ca:findById»(«pa:id», «st:"eur»«esc:\\n»«st:"»);
    }
}""")

GROOVY = ("OrderSpec.groovy", None, """\
«kw:class» «ty:OrderSpec» «kw:extends» «ty:Specification» {

    «kw:def» «st:"saves an order"»() {
        «lb:given:»
        «kw:def» order = «kw:new» «ty:Order»(«nu:7L», «nu:3»)
        «lb:when:»
        «kw:def» saved = «fd:repository».«ca:save»(order)
        «lb:then:»
        saved.«fd:quantity» == «nu:3»
    }
}""")

PYTHON = ("orders.py", None, """\
«an:@dataclass»
«kw:class» «ty:Order»:
    quantity: «PY.BUILTIN_NAME:int» = «nu:0»

    «kw:def» «fn:total»(«PY.SELF_PARAMETER:self», «pa:price»: «PY.BUILTIN_NAME:float») -> «PY.BUILTIN_NAME:float»:
        «doc:\"\"\"Price for the whole order.\"\"\"»
        «kw:return» «PY.SELF_PARAMETER:self».quantity * «pa:price»

«kw:if» «PY.PREDEFINED_USAGE:__name__» == «st:"__main__"»:
    «cm:# »«todo:TODO: read orders from a file»
    «PY.BUILTIN_NAME:print»(«ty:Order»(«PY.KEYWORD_ARGUMENT:quantity»=«nu:3»).«ca:total»(«nu:9.5»))""")

TYPESCRIPT = ("cart.ts", None, """\
«kw:const» «JS.GLOBAL_VARIABLE:CURRENCY» = «JS.REGEXP:/^[A-Z]{3}$/»;

«kw:export interface» «it:Item» {
  «fd:name»: «kw:string»;
  «fd:price»: «kw:number»;
}

«kw:export function» «JS.GLOBAL_FUNCTION:total»<«TS.TYPE_PARAMETER:T» «kw:extends» «it:Item»>(«pa:items»: «TS.TYPE_PARAMETER:T»[]) {
  «kw:const» «JS.LOCAL_VARIABLE:sum» = «pa:items».«ca:reduce»((«pa:s», «pa:i») => «pa:s» + «pa:i».«fd:price», «nu:0»);
  «kw:return» «ty:Math».«ca:round»(«JS.LOCAL_VARIABLE:sum» * «nu:100») / «nu:100»;
}""")

GO = ("order.go", None, """\
«kw:package» orders

«kw:type» «ty:Order» «kw:struct» {
    «fd:ID»       «ty:int»
    «fd:Quantity» «ty:int»
}

«cm:// Total returns the price of the whole order.»
«kw:func» («pa:o» «ty:Order») «fn:Total»(«pa:price» «ty:float64») «ty:float64» {
    «kw:return» «ty:float64»(«pa:o».«fd:Quantity») * «pa:price»
}""")

RUST = ("order.rs", None, """\
«an:#[derive(Debug)]»
«kw:pub struct» «ty:Order»<«org.rust.LIFETIME:'a»> {
    «fd:sku»: &«org.rust.LIFETIME:'a» «kw:str»,
    «fd:quantity»: «kw:u32»,
}

«kw:impl» «ty:Order»<«org.rust.LIFETIME:'_»> {
    «kw:pub fn» «fn:total»(&«kw:self», «pa:price»: «kw:f64») -> «kw:f64» {
        «org.rust.MACRO:println!»(«st:"»«esc:{}»«st: x »«esc:{}»«st:"», «kw:self».«fd:sku», «pa:price»);
        «kw:self».«fd:quantity» «kw:as» «kw:f64» * «pa:price»
    }
}""")

CPP = ("order.cpp", None, """\
«kw:#include» «st:<vector>»

«kw:struct» «ty:Order» {
    «kw:int» «fd:quantity»;
    «kw:double» «fd:price»;
};

«kw:double» «fn:total»(«kw:const» «ty:std»::«ty:vector»<«ty:Order»>& «pa:orders») {
    «kw:double» sum = «nu:0.0»;
    «kw:for» («kw:const auto»& o : «pa:orders»)
        sum += o.«fd:quantity» * o.«fd:price»;
    «kw:return» sum;
}""")

C = ("order.c", None, """\
«kw:#include» «st:<stdio.h>»
«kw:#define» «co:MAX_ITEMS» «nu:42»

«kw:typedef struct» { «kw:int» «fd:id»; «kw:int» «fd:quantity»; } «ty:order_t»;

«kw:int» «fn:main»(«kw:void») {
    «ty:order_t» order = { «nu:7», «nu:3» };
    «ca:printf»(«st:"order »«esc:%d»«st:, quantity »«esc:%d\\n»«st:"»,
           order.«fd:id», order.«fd:quantity»);
    «kw:return» «nu:0»;
}""")

CSHARP = ("OrderService.cs", None, """\
«kw:namespace» Shop;

«kw:public record» «ty:Order»(«kw:int» «pa:Id», «kw:int» «pa:Quantity»);

«kw:public class» «ty:OrderService»
{
    «kw:private readonly» «ty:List»<«ty:Order»> «fd:_orders» = «kw:new»();

    «kw:public int» «fn:Count»() => «fd:_orders».«fd:Count»;

    «kw:public void» «fn:Add»(«ty:Order» «pa:order») => «fd:_orders».«ca:Add»(«pa:order»);
}""")

SQL = ("orders.sql", None, """\
«cm:-- Customers who ordered more than ten items»
«kw:SELECT» c.«fd:id», c.«fd:name», «ca:SUM»(o.«fd:quantity») «kw:AS» total
«kw:FROM» customers c
«kw:JOIN» orders o «kw:ON» o.«fd:customer_id» = c.«fd:id»
«kw:WHERE» o.«fd:created_at» >= «st:'2026-01-01'»
«kw:GROUP BY» c.«fd:id», c.«fd:name»
«kw:HAVING» «ca:SUM»(o.«fd:quantity») > «nu:10»
«kw:ORDER BY» total «kw:DESC»
«kw:LIMIT» «nu:20»;""")

HTML = ("index.html", None, """\
«ht:<!DOCTYPE html>»
«ht:<»«hn:html» «ha:lang»«ht:=»«hv:"en"»«ht:>»
«ht:<»«hn:body»«ht:>»
  «bc:<!-- Order summary -->»
  «ht:<»«hn:main» «ha:class»«ht:=»«hv:"order"» «ha:data-id»«ht:=»«hv:"7"»«ht:>»
    «ht:<»«hn:h1»«ht:>»«txt:Order #7»«ht:</»«hn:h1»«ht:>»
    «ht:<»«hn:p»«ht:>»«txt:Total: »«he:&euro;»«txt:28.50»«ht:</»«hn:p»«ht:>»
    «ht:<»«hc:order-items» «ha:currency»«ht:=»«hv:"EUR"»«ht:></»«hc:order-items»«ht:>»
  «ht:</»«hn:main»«ht:>»
«ht:</»«hn:body»«ht:>»
«ht:</»«hn:html»«ht:>»""")

CSS = ("order.css", None, """\
«bc:/* Order card */»
«CSS.CLASS_NAME:.order» «CSS.TAG_NAME:h1»«CSS.PSEUDO::hover» {
  «CSS.PROPERTY_NAME:color»«CSS.COLON::» «CSS.COLOR:#B03A2E»;
  «CSS.PROPERTY_NAME:margin»«CSS.COLON::» «CSS.NUMBER:0» «CSS.NUMBER:1.5»«CSS.UNIT:rem»;
  «CSS.PROPERTY_NAME:font-family»«CSS.COLON::» «CSS.STRING:"JetBrains Mono"», «CSS.PROPERTY_VALUE:monospace»;
  «CSS.PROPERTY_NAME:background»«CSS.COLON::» «CSS.FUNCTION:url»(«CSS.URL:paper.png»);
  «CSS.PROPERTY_NAME:display»«CSS.COLON::» «CSS.PROPERTY_VALUE:grid» «CSS.IMPORTANT:!important»;
}""")

KOTLIN = ("Order.kt", None, """\
«kw:data class» «ty:Order»(«kw:val» «fd:id»: «ty:Long», «kw:val» «fd:quantity»: «ty:Int»)

«kw:fun» «ty:List»<«ty:Order»>.«fn:total»(«pa:price»: «ty:Double»): «ty:Double» =
    «KOTLIN_EXTENSION_FUNCTION_CALL:sumOf» «KOTLIN_FUNCTION_LITERAL_BRACES_AND_ARROW:{» «KOTLIN_CLOSURE_DEFAULT_PARAMETER:it».«fd:quantity» * «pa:price» «KOTLIN_FUNCTION_LITERAL_BRACES_AND_ARROW:}»

«kw:fun» «fn:main»() {
    «kw:var» «KOTLIN_MUTABLE_VARIABLE:count» = «nu:0»
    «kw:val» orders = «KOTLIN_PACKAGE_FUNCTION_CALL:listOf»(«ty:Order»(«nu:7», «KOTLIN_NAMED_ARGUMENT:quantity» = «nu:3»))
    orders.«KOTLIN_EXTENSION_FUNCTION_CALL:forEach» «KOTLIN_FUNCTION_LITERAL_BRACES_AND_ARROW:{» «KOTLIN_MUTABLE_VARIABLE:count»++ «KOTLIN_FUNCTION_LITERAL_BRACES_AND_ARROW:}»
    «KOTLIN_PACKAGE_FUNCTION_CALL:println»(orders.«ca:total»(«nu:9.5»))
}""")

TSX = ("OrderList.tsx", None, """\
«kw:import» { useState } «kw:from» «st:"react"»;

«kw:export function» «JS.GLOBAL_FUNCTION:OrderList»({ «pa:orders» }: «it:Props») {
  «kw:const» [«JS.LOCAL_VARIABLE:open», «JS.LOCAL_VARIABLE:setOpen»] = «ca:useState»(«kw:false»);
  «kw:return» (
    «XML_TAG:<»«XML_TAG_NAME:ul» «XML_ATTRIBUTE_NAME:hidden»«XML_TAG:=»{«JS.LOCAL_VARIABLE:open»}«XML_TAG:>»
      {«pa:orders».«ca:map»((«pa:o») => (
        «XML_TAG:<»«XML_TAG_NAME:OrderRow» «XML_ATTRIBUTE_NAME:key»«XML_TAG:=»{«pa:o».«fd:id»} «XML_TAG:/>»
      ))}
    «XML_TAG:</»«XML_TAG_NAME:ul»«XML_TAG:>»
  );
}""")

VUE = ("OrderCard.vue", None, """\
«ht:<»«hn:template»«ht:>»
  «ht:<»«hn:ul»«ht:>»
    «ht:<»«hn:li» «ha:v-for»«ht:=»«hv:"»«pa:o» «kw:in» «fd:orders»«hv:"» «ha::key»«ht:=»«hv:"»«pa:o».«fd:id»«hv:"»«ht:>»
      «op:{{» «pa:o».«fd:name» «op:}}»
    «ht:</»«hn:li»«ht:>»
  «ht:</»«hn:ul»«ht:>»
«ht:</»«hn:template»«ht:>»

«ht:<»«hn:script» «ha:setup» «ha:lang»«ht:=»«hv:"ts"»«ht:>»
«ca:defineProps»<{ «fd:orders»: «it:Order»[] }>();
«ht:</»«hn:script»«ht:>»""")

SHELL = ("deploy.sh", None, """\
«BASH.SHEBANG:#!/usr/bin/env bash»
«BASH.INTERNAL_COMMAND:set» «txt:-euo pipefail»

«BASH.FUNCTION_DEF_NAME:deploy»() {
  «BASH.INTERNAL_COMMAND:local» «BASH.VAR_DEF:target»=«st:"»«BASH.VAR_USE:$1»«st:"»
  «kw:if» [[ «txt:-z» «st:"»«BASH.VAR_USE:$target»«st:"» ]]; «kw:then»
    «BASH.INTERNAL_COMMAND:echo» «st:"no target"» >&«nu:2»; «BASH.INTERNAL_COMMAND:exit» «nu:1»
  «kw:fi»
  «BASH.EXTERNAL_COMMAND:rsync» «txt:-a build/» «st:"deploy@»«BASH.VAR_USE:$target»«st::/srv/orders"»
}

«BASH.FUNCTION_CALL:deploy» «st:"»«BASH.VAR_USE:$@»«st:"»""")

YAML = ("application.yml", None, """\
«YAML_COMMENT:# Micronaut configuration»
«YAML_SCALAR_KEY:micronaut»«YAML_SIGN::»
  «YAML_SCALAR_KEY:application»«YAML_SIGN::»
    «YAML_SCALAR_KEY:name»«YAML_SIGN::» «YAML_SCALAR_VALUE:orders»
  «YAML_SCALAR_KEY:server»«YAML_SIGN::»
    «YAML_SCALAR_KEY:port»«YAML_SIGN::» «YAML_SCALAR_VALUE:8080»
«YAML_SCALAR_KEY:datasources»«YAML_SIGN::»
  «YAML_SCALAR_KEY:default»«YAML_SIGN::» «YAML_ANCHOR:&db»
    «YAML_SCALAR_KEY:url»«YAML_SIGN::» «YAML_SCALAR_DSTRING:"jdbc:postgresql://localhost/orders"»
    «YAML_SCALAR_KEY:schema-generate»«YAML_SIGN::» «YAML_SCALAR_VALUE:NONE»""")

JSON = ("package.json", None, """\
{
  «JSON.PROPERTY_KEY:"name"»: «JSON.STRING:"orders-web"»,
  «JSON.PROPERTY_KEY:"private"»: «JSON.KEYWORD:true»,
  «JSON.PROPERTY_KEY:"version"»: «JSON.STRING:"1.4.0"»,
  «JSON.PROPERTY_KEY:"scripts"»: {
    «JSON.PROPERTY_KEY:"build"»: «JSON.STRING:"vite build"»
  },
  «JSON.PROPERTY_KEY:"engines"»: { «JSON.PROPERTY_KEY:"node"»: «JSON.STRING:">=22"» },
  «JSON.PROPERTY_KEY:"workspaces"»: [«JSON.STRING:"apps/*"»],
  «JSON.PROPERTY_KEY:"port"»: «JSON.NUMBER:5173»
}""")

TOML = ("Cargo.toml", None, """\
«cm:# Rust package manifest»
[«kw:package»]
«kw:name» = «st:"orders"»
«kw:version» = «st:"0.4.0"»
«kw:edition» = «st:"2024"»
«kw:publish» = «ps:false»

[«kw:dependencies»]
«kw:serde» = { «kw:version» = «st:"1"», «kw:features» = [«st:"derive"»] }
«kw:tokio» = «st:"1.45"»""")

MARKDOWN = ("README.md", None, """\
«MARKDOWN_HEADER_MARKER:#» «MARKDOWN_HEADER_LEVEL_1:Orders»

«txt:Tracks »«MARKDOWN_BOLD_MARKER:**»«MARKDOWN_BOLD:customer orders»«MARKDOWN_BOLD_MARKER:**»«txt: from cart to »«MARKDOWN_ITALIC_MARKER:_»«MARKDOWN_ITALIC:delivery»«MARKDOWN_ITALIC_MARKER:_»«txt:.»

«MARKDOWN_HEADER_MARKER:##» «MARKDOWN_HEADER_LEVEL_2:Run»

«MARKDOWN_LIST_MARKER:-» «txt:Start the API: »«MARKDOWN_CODE_SPAN_MARKER:`»«MARKDOWN_CODE_SPAN:./gradlew run»«MARKDOWN_CODE_SPAN_MARKER:`»
«MARKDOWN_LIST_MARKER:-» «txt:See »«MARKDOWN_LINK_TEXT:[the guide]»«txt:(»«MARKDOWN_LINK_DESTINATION:docs/guide.md»«txt:)»

«MARKDOWN_CODE_FENCE_MARKER:```»«MARKDOWN_CODE_FENCE_LANGUAGE:bash»
«MARKDOWN_CODE_FENCE:curl localhost:8080/orders»
«MARKDOWN_CODE_FENCE_MARKER:```»""")

SAMPLES = [JAVA, KOTLIN, GROOVY, PYTHON, TYPESCRIPT, TSX, VUE, HTML, CSS, SQL, GO, RUST, CPP, C, CSHARP, SHELL,
           YAML, JSON, TOML, MARKDOWN]
