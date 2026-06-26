# Shared Kernel Template for /forge (v3.53.1)

When user requests `--shared-kernel yes` (default if multi-platform), generate this project structure:

## Project: {name}.Shared

```xml
<!-- {name}.Shared.csproj -->
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net10.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <RootNamespace>{name}.Shared</RootNamespace>
    <AssemblyName>{name}.Shared</AssemblyName>
    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
  </PropertyGroup>
</Project>
```

## Folder Structure (13 subfolders)

```
src/{name}.Shared/
  Common/
    Result.cs              # Result Pattern (Ok<T> | Error)
    Error.cs               # Error type (code, message, type)
    PagedResult.cs         # Pagination wrapper
    BaseEntity.cs          # Base for DTOs (Id, CreatedAt, UpdatedAt)
    AuditableEntity.cs     # + CreatedBy, UpdatedBy
  DTOs/
    Customers/
      CustomerDto.cs
      CustomerSummaryDto.cs
    Orders/
      OrderDto.cs
      OrderItemDto.cs
  Enums/
    OrderStatus.cs         # Pending, Paid, Shipped, Delivered, Cancelled
    PaymentMethod.cs       # Card, Pix, Boleto, BankTransfer
    PaymentStatus.cs       # Pending, Paid, Failed, Refunded
    CustomerStatus.cs      # Active, Inactive, Suspended
  ValueObjects/
    Email.cs               # RFC 5322 validation
    Phone.cs               # BR format + international
    Money.cs               # Amount + Currency (ISO 4217)
    Cpf.cs                 # Brazil: 11 digits + mod-11 validation
    Cnpj.cs                # Brazil: 14 digits + mod-11 validation
  Interfaces/
    IDateTime.cs           # Abstraction for DateTime.UtcNow (testability)
    ICurrentUser.cs        # UserId, Roles, Claims abstraction
  Exceptions/
    DomainException.cs     # Base for domain errors
    NotFoundException.cs   # 404 semantic
    ValidationException.cs # 400 semantic with field errors
    ConflictException.cs   # 409 semantic
  Extensions/
    StringExtensions.cs    # ToSlug, IsNullOrEmpty, Truncate
    DateTimeExtensions.cs  # ToUnixTimestamp, StartOfDay, EndOfMonth
    CollectionExtensions.cs # IsNullOrEmpty, ForEach, ToPagedResult
  Requests/
    CreateCustomerRequest.cs
    UpdateCustomerRequest.cs
    PagedRequest.cs        # Page, PageSize, Sort, Filter
  Responses/
    ApiResponse.cs         # Success/Error wrapper
    ProblemDetailsExt.cs   # RFC 7807 extensions
  Events/
    CustomerCreatedEvent.cs
    CustomerUpdatedEvent.cs
    OrderPlacedEvent.cs
    OrderCancelledEvent.cs
  Constants/
    Roles.cs               # Admin, Manager, User, Guest
    Policies.cs            # CanEdit, CanDelete, CanView
  Validations/
    EmailValidator.cs      # FluentValidation reusable
    CpfValidator.cs        # BR CPF mod-11
    CnpjValidator.cs       # BR CNPJ mod-11
  Mappings/
    SharedMappingProfile.cs # AutoMapper shared profiles
```

## CRITICAL RULES (enforce)

1. **ZERO infra dependencies**: NO EF Core, NO HTTP, NO DI, NO JSON
2. **POCOs and records only**: no services, no managers, no logic beyond VOs
3. **TargetFramework net10.0**: compatible with WebApi + Blazor + MAUI + Desktop
4. **Nullable enable + TreatWarningsAsErrors**: strict null safety
5. **All Value Objects are immutable records** with validation in constructor
6. **All DTOs inherit BaseEntity**: consistent Id + audit fields
7. **No business logic**: only data shapes and value semantics
8. **AutoMapper Profile allowed**: pure mapping, no logic

## Example: Money Value Object

```csharp
namespace {name}.Shared.ValueObjects;

public readonly record struct Money(decimal Amount, string Currency)
{
    public static Money Zero(string currency = "BRL") => new(0m, currency);
    public static Money operator +(Money a, Money b)
    {
        if (a.Currency != b.Currency)
            throw new InvalidOperationException($"Cannot add {a.Currency} and {b.Currency}");
        return new Money(a.Amount + b.Amount, a.Currency);
    }
}
```

## Example: Result Pattern

```csharp
namespace {name}.Shared.Common;

public class Result<T>
{
    public bool IsSuccess { get; }
    public T? Value { get; }
    public Error? Error { get; }

    private Result(T value) { IsSuccess = true; Value = value; }
    private Result(Error error) { IsSuccess = false; Error = error; }

    public static Result<T> Ok(T value) => new(value);
    public static Result<T> Fail(Error error) => new(error);
}

public record Error(string Code, string Message, ErrorType Type);
public enum ErrorType { Validation, NotFound, Conflict, Unauthorized, Forbidden, Internal }
```

## Integration with other projects

```xml
<!-- In {name}.WebApi.csproj -->
<ProjectReference Include="..\{name}.Shared\{name}.Shared.csproj" />

<!-- In {name}.WebUI.csproj (Blazor) -->
<ProjectReference Include="..\{name}.Shared\{name}.Shared.csproj" />

<!-- In {name}.Maui.csproj (MAUI Hybrid) -->
<ProjectReference Include="..\{name}.Shared\{name}.Shared.csproj" />
```

## Auto-Apply Triggers

Add Shared Kernel automatically when:
- User requests `--shared-kernel yes`
- Multi-platform: WebApi + Blazor + MAUI + Desktop (4+ projects)
- User mentions "DRY", "shared code", "avoid duplication", "common library"
- Any project has DTOs that would be used in another project

Skip Shared Kernel when:
- Backend-only (single WebApi project)
- User explicitly says `--shared-kernel no`
- Project is microservice (independent deploy, no shared state)