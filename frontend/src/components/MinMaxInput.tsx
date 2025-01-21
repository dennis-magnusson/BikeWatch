import { useEffect, useState } from "react";
import { Input } from "./ui/input";

type MinMaxInputProps = {
    unit: string;
    minPrice: number;
    setMinPrice: React.Dispatch<React.SetStateAction<number>>;
    maxPrice: number;
    setMaxPrice: React.Dispatch<React.SetStateAction<number>>;
    validatePrices: () => void;
    hasError: boolean;
};

function MinMaxInput({
    unit,
    maxPrice,
    setMaxPrice,
    minPrice,
    setMinPrice,
    validatePrices,
    hasError,
}: MinMaxInputProps) {
    const [minPriceInput, setMinPriceInput] = useState<string>(
        minPrice.toString()
    );
    const [maxPriceInput, setMaxPriceInput] = useState<string>(
        maxPrice === Infinity ? "∞" : maxPrice.toString()
    );

    useEffect(() => {
        setMinPriceInput(minPrice.toString());
    }, [minPrice]);

    useEffect(() => {
        setMaxPriceInput(maxPrice === Infinity ? "∞" : maxPrice.toString());
    }, [maxPrice]);

    const handleMinPriceChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value;
        if (/^\d*$/.test(value)) {
            setMinPriceInput(value);
            setMinPrice(Number(value));
        } else {
            alert("Please enter only numeric values.");
        }
    };

    const handleMaxPriceChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value;
        if (/^\d*$/.test(value) || value === "∞") {
            setMaxPriceInput(value);
            setMaxPrice(value === "∞" ? Infinity : Number(value));
        } else {
            alert("Please enter only numeric values.");
        }
    };

    return (
        <div className="flex flex-col space-y-2">
            <div className="flex items-center space-x-2">
                <div className="relative">
                    <Input
                        value={minPriceInput}
                        onChange={handleMinPriceChange}
                        type="text"
                        placeholder="Min"
                        className={`pl-2 pr-8 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none max-w-32 ${
                            hasError ? "border-red-500" : ""
                        }`}
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
                        type="text"
                        placeholder="Max"
                        className={`pl-2 pr-8 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none max-w-32 ${
                            hasError ? "border-red-500" : ""
                        }`}
                    />
                    {unit && (
                        <span className="absolute right-2 top-1/2 -translate-y-1/2 text-gray-500">
                            €
                        </span>
                    )}
                </div>
            </div>
            {hasError && (
                <p className="text-sm text-red-500">
                    Min price cannot exceed max price.
                </p>
            )}
        </div>
    );
}

export default MinMaxInput;
