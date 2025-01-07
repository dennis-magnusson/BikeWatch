import { Check, MapPin, X } from "lucide-react";
import * as React from "react";

import { cn } from ".././lib/utils";
import { Location } from "../types";
import { Badge } from "./ui/badge";
import { Button } from "./ui/button";
import {
    Command,
    CommandEmpty,
    CommandGroup,
    CommandInput,
    CommandItem,
    CommandList,
} from "./ui/command";
import { Popover, PopoverContent, PopoverTrigger } from "./ui/popover";

type SearchableMultiselectProps = {
    locations: Location[];
    selectedValues: string[];
    setSelectedValues: React.Dispatch<React.SetStateAction<string[]>>;
};

function SearchableMultiselect({
    selectedValues,
    setSelectedValues,
    locations,
}: SearchableMultiselectProps) {
    const [open, setOpen] = React.useState(false);

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
                                {locations.map((location) => (
                                    <CommandItem
                                        key={location.value}
                                        value={location.value}
                                        onSelect={handleSelect}
                                    >
                                        {location.label}
                                        <Check
                                            className={cn(
                                                "ml-auto h-4 w-4",
                                                selectedValues.includes(
                                                    location.value
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
                    const framework = locations.find((l) => l.value === value);
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
