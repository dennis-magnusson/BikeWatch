import { Checkbox } from "./ui/checkbox";
import { Label } from "./ui/label";

type CheckboxGroupProps = {
    label: string;
    options: { id: string; value: string; label: string }[];
    selectedOptions: string[];
    setSelectedOptions: React.Dispatch<React.SetStateAction<string[]>>;
};

function CheckboxGroup({
    label,
    options,
    selectedOptions,
    setSelectedOptions,
}: CheckboxGroupProps) {
    const handleCheckboxChange = (value: string) => {
        console.log(value);
        setSelectedOptions((prev) =>
            prev.includes(value)
                ? prev.filter((option) => option !== value)
                : [...prev, value]
        );
    };

    return (
        <div>
            <div className="pb-3">
                <Label className="text-base">{label}</Label>
            </div>

            <div className="flex flex-row space-x-4">
                <div className="flex flex-col space-y-2">
                    {options.slice(0, 6).map((option) => (
                        <div
                            key={option.id}
                            className="flex items-center space-x-2"
                        >
                            <Checkbox
                                id={option.id}
                                value={option.value}
                                checked={selectedOptions.includes(option.value)}
                                onChange={() =>
                                    handleCheckboxChange(option.value)
                                }
                                className="h-5 w-5"
                            />
                            <Label
                                htmlFor={option.id}
                                className="text-base font-normal"
                            >
                                {option.label}
                            </Label>
                        </div>
                    ))}
                </div>

                <div className="flex flex-col space-y-2">
                    {options.slice(6).map((option) => (
                        <div
                            key={option.id}
                            className="flex items-center space-x-2"
                        >
                            <Checkbox
                                id={option.id}
                                value={option.value}
                                checked={selectedOptions.includes(option.value)}
                                onChange={() =>
                                    handleCheckboxChange(option.value)
                                }
                                className="h-5 w-5"
                            />
                            <Label
                                htmlFor={option.id}
                                className="text-base font-normal"
                            >
                                {option.label}
                            </Label>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}

export default CheckboxGroup;
