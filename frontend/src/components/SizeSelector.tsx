import { Checkbox } from "./ui/checkbox";
import { Input } from "./ui/input";
import { Label } from "./ui/label";

interface SizeSelectorProps {
    size: number;
    setSize: React.Dispatch<React.SetStateAction<number>>;
    showAllSizes: boolean;
    setShowAllSizes: React.Dispatch<React.SetStateAction<boolean>>;
    sizeFlexibility: boolean;
    setSizeFlexibility: React.Dispatch<React.SetStateAction<boolean>>;
}

export function SizeSelector({
    size,
    setSize,
    showAllSizes,
    setShowAllSizes,
    sizeFlexibility,
    setSizeFlexibility,
}: SizeSelectorProps) {
    return (
        <div className="space-y-2">
            <div className="flex items-center space-x-2">
                <div className="relative flex-1">
                    <Input
                        type="string"
                        value={size}
                        onChange={(e) => setSize(Number(e.target.value))}
                        disabled={showAllSizes}
                        className="pr-8 pl-2 w-full"
                    />
                    <span className="absolute right-3 top-1/2 -translate-y-1/2 text-sm text-gray-500">
                        cm
                    </span>
                </div>
                <div className="flex items-center space-x-2">
                    <Checkbox
                        id="allow-flexibility"
                        checked={sizeFlexibility}
                        onCheckedChange={(checked) =>
                            setSizeFlexibility(checked === true)
                        }
                        disabled={showAllSizes}
                    />
                    <Label htmlFor="allow-flexibility" className="text-sm">
                        Allow ±1 cm
                    </Label>
                </div>
            </div>
            <div className="flex items-center space-x-2">
                <Checkbox
                    id="disable-selection"
                    checked={showAllSizes}
                    onCheckedChange={(checked) =>
                        setShowAllSizes(checked === true)
                    }
                />
                <Label htmlFor="disable-selection" className="text-sm">
                    Show all sizes
                </Label>
            </div>
        </div>
    );
}
