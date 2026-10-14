"""Code samples for the preview, one per language, in pairs that share a row.

Markup: «key:text» highlights text with a text attribute key or an alias from heritage.preview.ALIASES.
Unmarked words use TEXT and unmarked punctuation uses DEFAULT_OPERATION_SIGN. Each sample is
(file name, line with the caret or None, code).
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

SAMPLES = [JAVA, GROOVY, PYTHON, TYPESCRIPT, GO, RUST, CPP, C, CSHARP, SQL, HTML, CSS]
