---
tags:
  - programming/snippets
---

Here's a snippet for replicating [[Rust]]'s `Result` enum as closely as possible in [[C++]]17+

```c++
// result.h

#include <iostream>
#include <variant>
#include <stdexcept>
#include <string>
#include <utility> // For std::forward

// std::monostate is how you would represent "void" in a std::variant
template <typename T = std::monostate, typename E = std::string>
class Result {
    // Variant to hold either the Ok value or the Err value
    std::variant<T, E> result;

private:
    // Private constructor for the static factory methods
    template <typename... Args>
    Result(std::in_place_index_t<0>, Args&&... args)
        : result(std::in_place_index<0>, std::forward<Args>(args)...) {}

    template <typename... Args>
    Result(std::in_place_index_t<1>, Args&&... args)
        : result(std::in_place_index<1>, std::forward<Args>(args)...) {}

public:
    // Type aliases for convenience
    using OkType = T;
    using ErrType = E;

    // Constructors for Ok and Err
    static Result Ok(T value = T()) {
        return Result(std::in_place_index<0>, std::move(value));
    }

    static Result Err(E error) {
        return Result(std::in_place_index<1>, std::move(error));
    }

    // Check if the result is Ok
    bool is_ok() const {
        return result.index() == 0;
    }

    // Check if the result is Err
    bool is_err() const {
        return result.index() == 1;
    }

    // Get the value if the result is Ok, throws if not
    T& unwrap() {
        if (is_ok()) {
            return std::get<0>(result);
        } else {
            throw std::runtime_error("Attempted to unwrap an Err value");
        }
    }

    const T& unwrap() const {
        if (is_ok()) {
            return std::get<0>(result);
        } else {
            throw std::runtime_error("Attempted to unwrap an Err value");
        }
    }

    // Get the error if the result is Err, throws if not
    E& unwrap_err() {
        if (is_err()) {
            return std::get<1>(result);
        } else {
            throw std::runtime_error("Attempted to unwrap an Ok value");
        }
    }

    const E& unwrap_err() const {
        if (is_err()) {
            return std::get<1>(result);
        } else {
            throw std::runtime_error("Attempted to unwrap an Ok value");
        }
    }

    // Operator-> to access the Ok value's methods
    T* operator->() {
        if (is_ok()) {
            return &std::get<0>(result);
        } else {
            throw std::runtime_error("Attempted to access an Err value");
        }
    }

    const T* operator->() const {
        if (is_ok()) {
            return &std::get<0>(result);
        } else {
            throw std::runtime_error("Attempted to access an Err value");
        }
    }

    // Operator* to access the Ok value directly
    T& operator*() {
        if (is_ok()) {
            return std::get<0>(result);
        } else {
            throw std::runtime_error("Attempted to access an Err value");
        }
    }

    const T& operator*() const {
        if (is_ok()) {
            return std::get<0>(result);
        } else {
            throw std::runtime_error("Attempted to access an Err value");
        }
    }
};

// Convenience function to create an Ok result
template <typename T = std::monostate, typename E = std::string>
Result<T, E> Ok(T value = T()) {
    return Result<T, E>::Ok(std::move(value));
}

// Convenience function to create an Err result
template <typename T = std::monostate, typename E = std::string>
Result<T, E> Err(E error) {
    return Result<T, E>::Err(std::move(error));
}

// Overload for const char* to std::string conversion
template <typename T = std::monostate>
Result<T, std::string> Err(const char* error) {
    return Result<T, std::string>::Err(std::string(error));
}

```

Here's an example on how you would use it:

```c++

// #include "result.h"

// Example class
class Foo {
public:
    void bar() const {
        std::cout << "Foo::bar() called" << std::endl;
    }
};

int main() {
    // Using default error type (std::string) and an empty Ok value
    Result<> result = Ok();

    if (result.is_ok()) {
        std::cout << "Ok" << std::endl;
    } else {
        std::cout << "Err: " << result.unwrap_err() << std::endl;
    }

    Result<> error_result = Err("Something went wrong");

    if (error_result.is_ok()) {
        std::cout << "Ok" << std::endl;
    } else {
        std::cout << "Err: " << error_result.unwrap_err() << std::endl;
    }

    // Using an int Ok value and default error type (std::string)
    Result<int> int_result = Ok(42);

    if (int_result.is_ok()) {
        std::cout << "Ok: " << *int_result << std::endl; // Using operator* to get the Ok value
    } else {
        std::cout << "Err: " << int_result.unwrap_err() << std::endl;
    }

    // Using a custom class with methods
    Result<Foo> foo_result = Ok(Foo());

    if (foo_result.is_ok()) {
        foo_result->bar(); // Using operator-> to call Foo's method
    } else {
        std::cout << "Err: " << foo_result.unwrap_err() << std::endl;
    }

    return 0;
}
