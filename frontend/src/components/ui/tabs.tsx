export function Tabs({ children, defaultValue, value, onValueChange, className = "" }: any) { return <div className={className}>{children}</div> } 
export function TabsList({ children, className = "" }: any) { return <div className={className}>{children}</div> } 
export function TabsTrigger({ children, value, className = "" }: any) { return <button value={value} className={className}>{children}</button> } 
export function TabsContent({ children, value, className = "" }: any) { return <div value={value} className={className}>{children}</div> } 
