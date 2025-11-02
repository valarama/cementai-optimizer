export function Dialog({ children, open, onOpenChange }: any) { return <div>{children}</div> } 
export function DialogTrigger({ children, asChild }: any) { return <div>{children}</div> } 
export function DialogContent({ children, className = "" }: any) { return <div className={className}>{children}</div> } 
export function DialogHeader({ children, className = "" }: any) { return <div className={className}>{children}</div> } 
export function DialogTitle({ children, className = "" }: any) { return <h2 className={className}>{children}</h2> } 
