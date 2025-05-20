# Quantum Computing and Cryptography Thesis

## Project Structure

```
.
├── src/                    # Source files
│   ├── chapters/          # LaTeX chapter files
│   ├── images/            # Image assets
│   ├── scripts/           # Utility scripts
│   └── bibliography/      # Bibliography files
├── docs/                  # Documentation
│   ├── thesis_workflow.md
│   ├── image_reference_guide.md
│   ├── progress_tracker.md
│   └── thesis_todo.md
├── build/                 # Build output directory
├── main.tex              # Main LaTeX file
├── preamble.tex          # LaTeX preamble
├── compile.sh            # Compilation script
└── README.md             # This file
```

## Building the Thesis

To compile the thesis, run:
```bash
./compile.sh
```

The output will be generated in the `build` directory.

## Documentation

All project documentation is located in the `docs` directory:
- `thesis_workflow.md`: Workflow and process documentation
- `image_reference_guide.md`: Guidelines for image usage and formatting
- `progress_tracker.md`: Project progress tracking
- `thesis_todo.md`: Current tasks and TODO items

## Contributing

1. Follow the academic writing standards defined in `.cursorrules`
2. Maintain proper LaTeX formatting and structure
3. Update documentation as needed
4. Use the provided scripts for compilation and progress tracking

## License

[Your License Here]