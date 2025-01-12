import { useState } from "react";
import { Input } from "./ui/input";

type MinMaxInputProps = {
    unit: string;
    minPrice: number;
    setMinPrice: React.Dispatch<React.SetStateAction<number>>;
    maxPrice: number;
    setMaxPrice: React.Dispatch<React.SetStateAction<number>>;
};

function MinMaxInput({
    unit,
    maxPrice,
    setMaxPrice,
    minPrice,
    setMinPrice,
}: MinMaxInputProps) {
    const [minPriceInput, setMinPriceInput] = useState<string>(
        minPrice.toString()
    );
    const [maxPriceInput, setMaxPriceInput] = useState<string>(
        maxPrice.toString()
    );

    const handleMinPriceChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setMinPriceInput(e.target.value);
        console.log(Number(e.target.value));
        setMinPrice(Number(e.target.value));
    };

    const handleMaxPriceChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setMaxPriceInput(e.target.value);
        console.log(Number(e.target.value));
        setMaxPrice(Number(e.target.value));
    };

    return (
        <div className="flex items-center space-x-2">
            <div className="relative">
                <Input
                    value={minPriceInput}
                    onChange={handleMinPriceChange}
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
                    value={maxPriceInput}
                    onChange={handleMaxPriceChange}
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
