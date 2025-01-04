import { Input } from "@/components/ui/input";

type MinMaxInputProps = {
    unit: string;
};

function MinMaxInput({ unit }: MinMaxInputProps) {
    return (
        <div className="flex items-center space-x-2">
            <div className="relative">
                <Input
                    type="number"
                    placeholder="Min"
                    className="pl-2 pr-8 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                />
                {unit && (
                    <span className="absolute right-2 top-1/2 -translate-y-1/2 text-gray-500">
                        {unit}
                    </span>
                )}
            </div>
            <span className="text-gray-500">-</span>
            <div className="relative">
                <Input
                    type="number"
                    placeholder="Max"
                    className="pl-2 pr-8 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                />
                {unit && (
                    <span className="absolute right-2 top-1/2 -translate-y-1/2 text-gray-500">
                        €
                    </span>
                )}
            </div>
        </div>
    );
}

export default MinMaxInput;
