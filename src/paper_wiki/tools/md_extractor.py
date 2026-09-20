class MD_Extractor():
    def __init__(self, file, filename):
        self.content = file
        self.filename = filename

    def get_sections(self)-> dict:
        self.sections = {}
        current_title = None
        current_content = []
        level_counters = {}
        current_number = ""

        for line in self.content.split('\n'):
            if line.startswith('#'):
                # Save previous section
                if current_title is not None:
                    self.sections[current_number] = {
                        "title": current_title,
                        "content": '\n'.join(current_content).strip()
                    }

                # Start new section
                level = len(line) - len(line.lstrip('#'))
                current_title = line.lstrip('#').strip()
                current_content = []

                # Update level counters for hierarchy
                level_counters[level] = level_counters.get(level, 0) + 1
                # Reset deeper levels
                keys_to_delete = [k for k in level_counters if k > level]
                for k in keys_to_delete:
                    del level_counters[k]

                # Build numbering (e.g., "1.2.3")
                current_number = '.'.join(str(level_counters[i]) for i in sorted(level_counters.keys()))
            else:
                if current_title is not None:
                    current_content.append(line)

        # Save last section
        if current_title is not None:
            self.sections[current_number] = {
                "title": current_title,
                "content": '\n'.join(current_content).strip()
            }

        return self.sections
