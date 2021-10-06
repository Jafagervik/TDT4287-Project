CXX_FLAGS := -Wall -Wextra -std=c++20 -ggdb

BIN         := bin
SRC         := src
INCLUDE     := include
LIBRARIES   := 
EXECUTABLE  := main

all: $(BIN)/$(EXECUTABLE)

run: clean all clear @echo "🚀 Executing..." ./$(BIN)/$(EXECUTABLE)

$(BIN)/$(EXECUTABLE): $(SRC)/*.cpp
	@echo "🚧 Building..."
	$(CC) $(CXX_FLAGS) -I$(INCLUDE) $^ -o $@ $(LIBRARIES)

clean:
	@echo "🧹 Cleaning..."
	-rm $(BIN)/*