import { Check, MapPin, X } from "lucide-react";
import * as React from "react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
    Command,
    CommandEmpty,
    CommandGroup,
    CommandInput,
    CommandItem,
    CommandList,
} from "@/components/ui/command";
import {
    Popover,
    PopoverContent,
    PopoverTrigger,
} from "@/components/ui/popover";
import { cn } from "@/lib/utils";

const frameworks = [
    {
        value: "region:uusimaa",
        label: "Uusimaa",
    },
    {
        value: "city:savonlinna",
        label: "Savonlinna",
    },
    {
        value: "city:Helsinki",
        label: "Helsinki",
    },
    {
        value: "city:vantaa",
        label: "Vantaa",
    },
    {
        value: "region:pirkanmaa",
        label: "Pirkanmaa",
    },
];

function SearchableMultiselect() {
    const [open, setOpen] = React.useState(false);
    const [selectedValues, setSelectedValues] = React.useState<string[]>([]);

    const handleSelect = (currentValue: string) => {
        setSelectedValues((prev) =>
            prev.includes(currentValue)
                ? prev.filter((value) => value !== currentValue)
                : [...prev, currentValue]
        );
    };

    const handleRemove = (valueToRemove: string) => {
        setSelectedValues((prev) =>
            prev.filter((value) => value !== valueToRemove)
        );
    };

    return (
        <div className="flex flex-col gap-2">
            <Popover open={open} onOpenChange={setOpen}>
                <PopoverTrigger asChild>
                    <Button
                        variant="outline"
                        role="combobox"
                        aria-expanded={open}
                        className="w-[200px] justify-between"
                    >
                        {selectedValues.length > 0
                            ? `${selectedValues.length} selected`
                            : "Filter by location"}
                        <MapPin className="ml-2 h-4 w-4 shrink-0 opacity-50" />
                    </Button>
                </PopoverTrigger>
                <PopoverContent className="w-[200px] p-0">
                    <Command>
                        <CommandInput
                            placeholder="Search cities & regions"
                            className="h-9"
                        />
                        <CommandList>
                            <CommandEmpty>No locations found</CommandEmpty>
                            <CommandGroup>
                                {frameworks.map((framework) => (
                                    <CommandItem
                                        key={framework.value}
                                        value={framework.value}
                                        onSelect={handleSelect}
                                    >
                                        {framework.label}
                                        <Check
                                            className={cn(
                                                "ml-auto h-4 w-4",
                                                selectedValues.includes(
                                                    framework.value
                                                )
                                                    ? "opacity-100"
                                                    : "opacity-0"
                                            )}
                                        />
                                    </CommandItem>
                                ))}
                            </CommandGroup>
                        </CommandList>
                    </Command>
                </PopoverContent>
            </Popover>
            <div className="flex flex-wrap gap-2">
                {selectedValues.map((value) => {
                    const framework = frameworks.find((f) => f.value === value);
                    return (
                        <Badge key={value} variant="secondary">
                            {framework?.label}
                            <Button
                                variant="ghost"
                                size="sm"
                                className="ml-1 h-auto p-0 text-muted-foreground hover:bg-transparent hover:text-foreground"
                                onClick={() => handleRemove(value)}
                            >
                                <X className="h-3 w-3" />
                                <span className="sr-only">Remove</span>
                            </Button>
                        </Badge>
                    );
                })}
            </div>
        </div>
    );
}

export default SearchableMultiselect;
